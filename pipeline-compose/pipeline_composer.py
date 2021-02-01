import os

import kfp

component_root = '../components/split_file/'

# Load the component by calling load_component_from_file or load_component_from_url
# To load the component, the pipeline author only needs to have access to the component.yaml file.
# The Kubernetes cluster executing the pipeline needs access to the container image specified in the component.
dummy_op = kfp.components.load_component_from_file(os.path.join(component_root, 'component.yaml'))


# Define a pipeline and create a task from a component:
def my_pipeline(input_path_pipeline: str, number_of_lines: int):
    dummy1_task = dummy_op(
        # Input name "Input 1" is converted to pythonic parameter name "input_1"
        input_path=input_path_pipeline,
        number_of_lines_to_split=number_of_lines,
        output_path="/tmp/output"
    )
    # The outputs of the dummy1_task can be referenced using the
    # dummy1_task.outputs dictionary: dummy1_task.outputs['output_1']
    # ! The output names are converted to pythonic ("snake_case") names.


kfp.compiler.Compiler().compile(my_pipeline, 'my-pipeline.zip')

# This pipeline can be compiled, uploaded and submitted for execution.
# kfp.Client().create_run_from_pipeline_func(my_pipeline, arguments={})
