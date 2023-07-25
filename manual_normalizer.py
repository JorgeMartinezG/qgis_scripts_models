import numpy as np
from qgis import processing
from qgis.PyQt.QtCore import QVariant
from qgis.processing import alg
from qgis.core import *


@alg(
    name="manual_normalizer",
    label="Normalize manually",
    group="risk_analysis",
    group_label="Risk analysis",
)
@alg.input(type=alg.SOURCE, name="INPUT", label="Input layer")
@alg.input(
    type=alg.STRING,
    name="COLUMN_NAME",
    label="Column name (value)",
    default="rwi_float_",
)
@alg.input(type=alg.NUMBER, name="MIN_VALUE", label="Min value")
@alg.input(type=alg.NUMBER, name="MAX_VALUE", label="Max value")
@alg.input(type=alg.SINK, name="OUTPUT", label="Output layer")
def normalize(instance, parameters, context, feedback, inputs):
    """
    Normalize
    """

    source = instance.parameterAsSource(parameters, "INPUT", context)
    column_name = instance.parameterAsString(
        parameters, "COLUMN_NAME", context
    )

    upper = instance.parameterAsDouble(parameters, "MAX_VALUE", context)
    lower = instance.parameterAsDouble(parameters, "MIN_VALUE", context)

    output_fields = source.fields()
    output_fields.append(QgsField(f"{column_name}_norm", QVariant.Double))
    output_fields.append(QgsField(f"{column_name}_minmax", QVariant.String))

    features = [f for f in source.getFeatures(QgsFeatureRequest())]
    values = [
        f.attribute(column_name)
        for f in features
        if isinstance(f.attribute(column_name), QVariant) is False
    ]
    mean_value = np.array(values).mean()
    # np_values = np.array(values)
    (sink, dest_id) = instance.parameterAsSink(
        parameters,
        "OUTPUT",
        context,
        output_fields,
        source.wkbType(),
        source.sourceCrs(),
    )

    """


    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1

    upper = Q3 + 1.5 * IQR
    lower = Q1 + 1.5 * IQR
    """

    for feat in features:
        out_feat = QgsFeature()
        out_feat.setFields(output_fields)
        out_feat.setGeometry(feat.geometry())
        value = (
            feat.attribute(column_name)
            if isinstance(feat.attribute(column_name), float)
            else mean_value
        )
        if value > upper:
            norm_value = 1
        elif value < lower:
            norm_value = 0.1
        else:
            norm_value = float((value - lower) / (upper - lower))

        out_feat.setAttributes(
            [*feat.attributes(), norm_value * 10, f"{lower}/{upper}"]
        )

        sink.addFeature(out_feat, QgsFeatureSink.FastInsert)

    return {"OUTPUT": dest_id}
