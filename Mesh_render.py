#
import sys
import torch
need_pytorch3d=False

import cv2
import pdb


try:
    import pytorch3d
except ModuleNotFoundError:
    need_pytorch3d=True
if need_pytorch3d:
    if torch.__version__.startswith("1.7") and sys.platform.startswith("linux"):
        # We try to install PyTorch3D via a released wheel.
        version_str="".join([
            f"py3{sys.version_info.minor}_cu",
            torch.version.cuda.replace(".",""),
            f"_pyt{torch.__version__[0:5:2]}"
        ])
        os.system('pip install pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/{version_str}/download.html')
    else:
        # We try to install PyTorch3D from source.
        os.system('curl -LO https://github.com/NVIDIA/cub/archive/1.10.0.tar.gz')
        os.system('tar xzf 1.10.0.tar.gz')
        os.environ["CUB_HOME"] = os.getcwd() + "/cub-1.10.0"
        os.system('pip install git+https://github.com/facebookresearch/pytorch3d.git@stable')



import os
from skimage.io import imread

# Util function for loading meshes
from pytorch3d.io import load_objs_as_meshes, load_obj

# Data structures and functions for rendering
from pytorch3d.structures import Meshes
from pytorch3d.vis.plotly_vis import AxisArgs, plot_batch_individually, plot_scene
from pytorch3d.vis.texture_vis import texturesuv_image_matplotlib
from pytorch3d.renderer import (
    look_at_view_transform,
    FoVPerspectiveCameras, 
    PerspectiveCameras,
    PointLights, 
    DirectionalLights, 
    Materials, 
    RasterizationSettings, 
    MeshRenderer, 
    MeshRasterizer,  
    SoftPhongShader,
    TexturesUV,
    TexturesVertex
)

# add path for demo utils functions 
import sys
import os
sys.path.append(os.path.abspath(''))

import os
from math import pi
from pytorch3d.transforms import axis_angle_to_matrix
sys.path.append(os.path.abspath(''))


# Loading Data



# Setup
if torch.cuda.is_available():
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)
else:
    device = torch.device("cpu")

# Set paths
DATA_DIR = "./data"
obj_filename = os.path.join(DATA_DIR, "Tile_+1984_+2690_groundtruth_L1.obj")

# Load obj file
mesh = load_objs_as_meshes([obj_filename], device=device)


T = torch.Tensor([6034.444325201213,4562.423854339868,11]).view([1,3]);


theta1 = 0 / 180 * pi    # pitch
theta2 = 0 / 180 * pi    # yaw
theta3 = 0 / 180 * pi     # roll

R = axis_angle_to_matrix(torch.Tensor([theta1,theta2,theta3]))
#TR = torch.Tensor([[0,0,1],[1,0,0],[0,1,0]])
TR = torch.Tensor([[-1,0,0],[0,0,1],[0,1,0]])
R = torch.matmul(TR,R)

R = R.view([1,3,3])
T = -torch.matmul(T,R).squeeze(0)
#T = -torch.matmul(R.transpose(1, 2), T.transpose(0,1)).squeeze(2)


#cameras = PerspectiveCameras(device=device, focal_length=((255,255),), principal_point=((320.0, 320.0),), image_size=((640,640),), R=R, T=T)
cameras = FoVPerspectiveCameras(device=device, fov=115.0, aspect_ratio=640./640., R=R, T=T)
# the difference between naive and coarse-to-fine rasterization. 
raster_settings = RasterizationSettings(
    image_size=(640,640), 
    blur_radius=0.0, 
    faces_per_pixel=10, 
)

# -z direction. 
lights = PointLights(device=device, ambient_color=((0.8, 0.8, 0.8), ))

# apply the Phong lighting model
renderer = MeshRenderer(
    rasterizer=MeshRasterizer(
        cameras=cameras, 
        raster_settings=raster_settings
    ),
    shader=SoftPhongShader(
        device=device, 
        cameras=cameras,
        lights=lights
    )
)




images = renderer(mesh)

for i,image in enumerate(images):
    img = image[...,:3].cpu().numpy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite('render_img_{}.png'.format(0), img*255)


print('Done')
