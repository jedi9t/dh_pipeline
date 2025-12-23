# Generating Digital Human Video with open source projects locally


<div align="left">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://zdoc.app/de/jedi9t/dh_pipeline">Deutsch</a> | 
  <a href="https://zdoc.app/es/jedi9t/dh_pipeline">Español</a> | 
  <a href="https://zdoc.app/fr/jedi9t/dh_pipeline">Français</a> | 
  <a href="https://zdoc.app/ja/jedi9t/dh_pipeline">日本語</a> | 
  <a href="https://zdoc.app/ko/jedi9t/dh_pipeline">한국어</a> | 
  <a href="https://zdoc.app/pt/jedi9t/dh_pipeline">Português</a> | 
  <a href="https://zdoc.app/ru/jedi9t/dh_pipeline">Русский</a> | 
  <a href="https://zdoc.app/en/jedi9t/dh_pipeline">English</a>
</div>


## 1. Enviroment preparation

> Create conda is strongly recommending
```bash
mkdir dh_pipeline
cd dh_pipeline
conda create -n dh_pipeline python=3.10 -y
conda activate dh_pipeline
```

## 2. Translation and voice generating
>Install Goolge deep translate and Microsoft EdgeTTS to translate conent from original languate to other language then generate sound accordingly.

```bash
pip install deep-translator edge-tts
```

>Run the translation and TTS gen
```bash
python run_tts.py
```

## 3. Video Combine
> Let static avator be moving along with the sample video that could be anyone's movement.

### a. Get soure of LivePortait
```bash
git clone https://github.com/KwaiVGI/LivePortrait
cd LivePortrait
```
### b. Install dependencies

<details> 
 <summary>Check your CUDA versions!!!</summary>

```
nvcc -V # example versions: 11.1, 11.8, 12.1, etc.
```
Then, install the corresponding torch version. Here are examples for different CUDA versions. Visit the [PyTorch Official Website](https://pytorch.org/get-started/previous-versions) for installation commands if your CUDA version is not listed:
  ```bash  
  # for CUDA 11.8
  pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118

  # for CUDA 12.1
  pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
  # ...
  ```
  > You can check CUDA version in nvidia-smi, if the version higher than 11.8, just use the # for CUDA 11.8 or above, keep the torch version on 2.1.2, otherwise would be conflict with MuseTalk!!!

  **Check Numpy, should not be great than 2.0, if so downgrade**
  ```
  # check Numpy version
  pip show numpy

  pip install "numpy==1.26.4"
  ```
</details>

install the remaining dependencies:

```bash
pip install -r requirements.txt
```

### c. Download pretrained weights 📥
The easiest way to download the pretrained weights is from HuggingFace:

```bash
# !pip install -U "huggingface_hub[cli]"
huggingface-cli download KlingTeam/LivePortrait --local-dir pretrained_weights --exclude "*.git*" "README.md" "docs"
```

If you cannot access to Huggingface, you can use hf-mirror to download:
```bash
# !pip install -U "huggingface_hub[cli]"
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download KlingTeam/LivePortrait --local-dir pretrained_weights --exclude "*.git*" "README.md" "docs"
```

Alternatively, you can download all pretrained weights from [Google Drive](https://drive.google.com/drive/folders/1UtKgzKjFAOmZkhNK-OYT0caJ_w2XAnib) or [Baidu Yun](https://pan.baidu.com/s/1MGctWmNla_vZxDbEp2Dtzw?pwd=z5cn). Unzip and place them in ./pretrained_weights.

Ensuring the directory structure is as or contains following.

> The directory structure of `pretrained_weights`

```text
pretrained_weights
├── insightface
│   └── models
│       └── buffalo_l
│           ├── 2d106det.onnx
│           └── det_10g.onnx
├── liveportrait
│   ├── base_models
│   │   ├── appearance_feature_extractor.pth
│   │   ├── motion_extractor.pth
│   │   ├── spade_generator.pth
│   │   └── warping_module.pth
│   ├── landmark.onnx
│   └── retargeting_models
│       └── stitching_retargeting_module.pth
└── liveportrait_animals
    ├── base_models
    │   ├── appearance_feature_extractor.pth
    │   ├── motion_extractor.pth
    │   ├── spade_generator.pth
    │   └── warping_module.pth
    ├── retargeting_models
    │   └── stitching_retargeting_module.pth
    └── xpose.pth
```

**Rock and Roll**
> default saved result at LivePortait/animations
```bash
 python inference.py
```

or with image and driving video path

```bash
python inference.py  --source "assets/examples/source/s12.jpg"   --driving "assets/examples/driving/d13.mp4" 
```

## 4. Mouse match

### a. Download code
```bash
git clone https://github.com/TMElyralab/MuseTalk.git
cd MuseTalk
```

### b. Install Dependencies

```bash
pip install -r requirements.txt

# Make sure numpy is lower than 2.0
# pip install "numpy==1.26.4"

# Make sure torch is 2.1.2, 
#pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118

# make sure the verison of mmcv is following:
wget https://download.openmmlab.com/mmcv/dist/cu118/torch2.1.0/mmcv-2.1.0-cp310-cp310-manylinux1_x86_64.whl

pip install mmcv-2.1.0-cp310-cp310-manylinux1_x86_64.whl

# Strickly limit version of rest dependencies
pip install "transformers==4.37.2" "diffusers==0.24.0" "accelerate==0.26.0" "huggingface-hub==0.23.5" "tokenizers==0.15.2" "opencv-python-headless==4.9.0.80" "omegaconf" "imageio-ffmpeg" "av" "scipy"

# Finally install OpenMMLab components
pip install "mmengine>=0.10.0" "mmpose>=1.1.0" "mmdet>=3.1.0"

# verify
python -c "import torch; import cv2; import numpy; from mmcv.ops import MultiScaleDeformableAttention; print(f'✅ Perfect enviroment: Torch={torch.__version__}, NumPy={numpy.__version__}, MMCV OK')"
```

> if now show ' ✅ Perfect enviroment: Torch=2.1.2+cu118, NumPy=1.26.4, MMCV O', please start over!!!

### c. Download weights
You can download weights in two ways:

#### Option 1: Using Download Scripts
We provide two scripts for automatic downloading:

For Linux:
```bash
sh ./download_weights.sh
```

For Windows:
```batch
# Run the script
download_weights.bat
```

You can also download the weights manually from the following links:

1. Download our trained [weights](https://huggingface.co/TMElyralab/MuseTalk/tree/main)
2. Download the weights of other components:
   - [sd-vae-ft-mse](https://huggingface.co/stabilityai/sd-vae-ft-mse/tree/main)
   - [whisper](https://huggingface.co/openai/whisper-tiny/tree/main)
   - [dwpose](https://huggingface.co/yzd-v/DWPose/tree/main)
   - [syncnet](https://huggingface.co/ByteDance/LatentSync/tree/main)
   - [face-parse-bisent](https://drive.google.com/file/d/154JgKpzCPW82qINcVieuPH3fZ2e0P812/view?pli=1)
   - [resnet18](https://download.pytorch.org/models/resnet18-5c106cde.pth)

Finally, these weights should be organized in `models` as follows:
```
./models/
├── musetalk
│   └── musetalk.json
│   └── pytorch_model.bin
├── musetalkV15
│   └── musetalk.json
│   └── unet.pth
├── syncnet
│   └── latentsync_syncnet.pt
├── dwpose
│   └── dw-ll_ucoco_384.pth
├── face-parse-bisent
│   ├── 79999_iter.pth
│   └── resnet18-5c106cde.pth
├── sd-vae
│   ├── config.json
│   └── diffusion_pytorch_model.bin
└── whisper
    ├── config.json
    ├── pytorch_model.bin
    └── preprocessor_config.json
    
```


### d. Rock and Roll
```bash
sh inference.sh v1.5 realtime
```