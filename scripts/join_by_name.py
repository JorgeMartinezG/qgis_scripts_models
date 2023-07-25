import pandas as pd
from difflib import SequenceMatcher
from functools import reduce
from qgis import processing
from qgis.PyQt.QtCore import QVariant
from qgis.processing import alg
from qgis.core import *

MASTER_LAYER = "MASTER_LAYER"
FILE_NAME = "FILE_NAME"
MASTER_COLUMN_NAME = "MASTER_COLUMN_NAME"
FILE_COLUMN_NAME = "FILE_COLUMN_NAME"
THRESOLD = "THRESHOLD"
OUTPUT = "OUTPUT"


def feature_to_dict(qgs_feature):
    feature_fields = [field.name() for field in qgs_feature.fields().toList()]
    return {f: qgs_feature.attribute(f) for f in feature_fields}


def match_score(word_1, word_2):
    return SequenceMatcher(None, word_1, word_2).ratio()


@alg(
    name="join_by_name",
    label="Join data by column names",
    group="risk_analysis",
    group_label="Risk analysis",
)
@alg.input(
    type=alg.SOURCE,
    name=MASTER_LAYER,
    label="Master layer",
    default="/Users/jorgemartinez/data/wfp/risk_analysis/ECU/ecu_bnd_adm2_ge/ecu_bnd_adm2_ge.shp",
)
@alg.input(
    type=alg.SOURCE,
    name=FILE_NAME,
    label="File name",
    default="/Users/jorgemartinez/Desktop/gsap_errors.xlsx",
)
@alg.input(
    type=alg.STRING,
    name=MASTER_COLUMN_NAME,
    label="Master column name",
    default="adm1_name",
)
@alg.input(
    type=alg.STRING,
    name=FILE_COLUMN_NAME,
    label="File column name",
    default="adm1_name",
)
@alg.input(type=alg.DISTANCE, name=THRESOLD, label="Threshold", default=0.8)
@alg.input(type=alg.SINK, name=OUTPUT, label="Output layer")
def location_resolution_tool(instance, parameters, context, feedback, inputs):
    """
    Join by column name
    """
    master_layer = instance.parameterAsSource(
        parameters, MASTER_LAYER, context
    )
    master_column_name = instance.parameterAsString(
        parameters, MASTER_COLUMN_NAME, context
    )

    file_source = instance.parameterAsSource(parameters, FILE_NAME, context)
    file_column_name = instance.parameterAsString(
        parameters, FILE_COLUMN_NAME, context
    )
    threshold = instance.parameterAsDouble(parameters, THRESOLD, context)

    # Adding additional columns from excel file.
    file_fields = file_source.fields().toList()
    output_fields = master_layer.fields()
    columns_to_append = [
        f for f in file_fields if f.name() != file_column_name
    ]
    [output_fields.append(c) for c in columns_to_append]

    file_list = [
        feature_to_dict(f)
        for f in file_source.getFeatures(QgsFeatureRequest())
    ]

    (sink, dest_id) = instance.parameterAsSink(
        parameters,
        OUTPUT,
        context,
        output_fields,
        master_layer.wkbType(),
        master_layer.sourceCrs(),
    )

    features_iter = master_layer.getFeatures(QgsFeatureRequest())
    cache = {}
    for feature in features_iter:
        master_value = feature.attribute(master_column_name)

        if master_value not in cache.keys():
            match_scores_list = [
                {
                    **i,
                    "score": match_score(master_value, i[file_column_name]),
                    "row": r + 2,
                }
                for r, i in enumerate(file_list)
            ]
            sorted_matched_scores = sorted(
                match_scores_list,
                key=lambda x: x["score"],
                reverse=True,
            )

            # Pick match with highest score.
            closest_match = sorted_matched_scores[0]
            cache[master_value] = closest_match
        else:
            closest_match = cache[master_value]
        closest_score = closest_match["score"]

        # Report conflict.
        closest_value = closest_match[file_column_name]
        closest_row = closest_match["row"]

        out_feat = QgsFeature()
        out_feat.setFields(output_fields)
        out_feat.setGeometry(feature.geometry())

        # Get missing value from closest match.
        missing_values = [
            closest_match[c.name()] if closest_score >= threshold else None
            for c in columns_to_append
        ]
        out_feat.setAttributes([*feature.attributes(), *missing_values])

        sink.addFeature(out_feat, QgsFeatureSink.FastInsert)

        if closest_score == 1.0:
            continue

        closest_score_format = "{:.2f}".format(closest_score)
        message = f"STATUS=CONFLICT MASTER_VALUE='{master_value}' ROW={closest_row} SCORE={closest_score_format} CLOSEST_VALUE='{closest_value}'"
        if closest_score < threshold:
            feedback.reportError(message)
            continue

        feedback.pushConsoleInfo(message)

    return {OUTPUT: dest_id}
