import os
import yaml

MODEL_SPEC_FILE_NAME = "model_spec.yml"


class BuiltinScoreModule(object):

    def __init__(self, model_path, params={}):
        model_spec_path = os.path.join(model_path, MODEL_SPEC_FILE_NAME)
        with open(model_spec_path) as fp:
            config = yaml.safe_load(fp)

        model_file_path = os.path.join(model_path, config["model_file_path"])
        framework = config["flavor"]["framework"]
        if framework.lower() == "pytorch":
            from .pytorch_score_module import PytorchScoreModule
            self.module = PytorchScoreModule(model_file_path)
        elif framework.lower() == "tensorflow":
            from .tensorflow_score_module import TensorflowScoreModule
            self.module = TensorflowScoreModule(model_file_path)
        else:
            print(f"Not Implemented: framework {framework} not supported")

    def run(self, df, global_param=None):
        output_label = self.module.run(df)
        print(output_label)

        df.insert(len(df.columns), "Scored Label", output_label, True)
        return df
