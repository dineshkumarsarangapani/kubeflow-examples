import os

import kfp
from kfp import dsl

component_root = '../../components/minst-example/'

train_root = "train"
predict_root = "predict"
# Load the component by calling load_component_from_file or load_component_from_url
# To load the component, the pipeline author only needs to have access to the component.yaml file.
# The Kubernetes cluster executing the pipeline needs access to the container image specified in the component.
train_op = kfp.components.load_component_from_file(os.path.join(component_root, train_root, 'component.yaml'))


# Define a pipeline and create a task from a component:
@dsl.pipeline(
    name='MNIST Pipeline by container',
    description='A toy pipeline that performs mnist model training and prediction.'
)
def mist_pipeline(data_path: str, model_file_name: str):
    vop = dsl.VolumeOp(
        name="mypvc",
        resource_name="newpvc",
        size="1Gi",
        modes=dsl.VOLUME_MODE_RWM
    )

    train_task = train_op(
        # Input name "Input 1" is converted to pythonic parameter name "input_1"
        data_path=data_path,
        model_file=model_file_name,
    )
        #.add_pvolumes({data_path: vop.volume})
    # The outputs of the dummy1_task can be referenced using the
    # dummy1_task.outputs dictionary: dummy1_task.outputs['output_1']
    # ! The output names are converted to pythonic ("snake_case") names.
    # Print the result of the prediction
    mnist_result_container = dsl.ContainerOp(
        name="print_prediction",
        image='library/bash:4.4.23',
        arguments=['ls', f'/']
    )


kfp.compiler.Compiler().compile(mist_pipeline, 'mist-pipeline.zip')

# This pipeline can be compiled, uploaded and submitted for execution.
# kfp.Client().create_run_from_pipeline_func(my_pipeline, arguments={})
