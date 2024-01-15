import yaml
from pathlib import Path
import torch.optim.adam  # for Adam optimizer

# Nerfstudio imports
from nerfstudio.engine.trainer import TrainerConfig, Trainer
from nerfstudio.configs.base_config import LoggingConfig, LocalWriterConfig, MachineConfig, ViewerConfig
from nerfstudio.utils.writer import LocalWriter, EventName
from nerfstudio.engine.optimizers import AdamOptimizerConfig
from nerfstudio.engine.schedulers import ExponentialDecayScheduler, ExponentialDecaySchedulerConfig
from nerfstudio.pipelines.base_pipeline import VanillaPipelineConfig, VanillaPipeline
from nerfstudio.data.datamanagers.base_datamanager import VanillaDataManagerConfig, VanillaDataManager
from nerfstudio.cameras.camera_optimizers import CameraOptimizerConfig, CameraOptimizer
from nerfstudio.data.utils.nerfstudio_collate import nerfstudio_collate
from nerfstudio.data.dataparsers.nerfstudio_dataparser import NerfstudioDataParserConfig, Nerfstudio
from nerfstudio.data.pixel_samplers import PixelSamplerConfig, PixelSampler
from nerfstudio.models.nerfacto import NerfactoModelConfig, NerfactoModel


# Load the YAML file
with open('outputs/data/nerfacto/2024-01-15_060326/config.yml', 'r') as file:
    nerf_config = yaml.load(file, Loader=yaml.FullLoader)

# Now `nerf_config` should be an instance of the deserialized Python object
print(nerf_config)