# All-in-One Digital Human Video Pipeline
<p align="center">
  <img src="https://raw.githubusercontent.com/mota-techlink/dh_pipeline/refs/heads/main/assets/images/cover.jpg" alt="MOTA dh_pipeline">
</p>

A modular and high-efficiency pipeline designed to generate realistic digital human videos locally. It integrates LivePortrait for motion synchronization and MuseTalk for precise lip-sync, powered by MOTA TECHLINK's optimization logic.


<div align="left">
  <!-- Keep these links. Translations will automatically update with the README. -->  
  <a href="https://zdoc.app/zh/mota-techlink/dh_pipeline">中文</a> | 
  <a href="https://zdoc.app/es/mota-techlink/dh_pipeline">Español</a> |  
  <a href="https://zdoc.app/de/mota-techlink/dh_pipeline">Deutsch</a> | 
  <a href="https://zdoc.app/fr/mota-techlink/dh_pipeline">Français</a> |      
  <a href="https://zdoc.app/pt/mota-techlink/dh_pipeline">Português</a> |   
  <a href="https://zdoc.app/ru/mota-techlink/dh_pipeline">Русский</a> |   
  <a href="https://zdoc.app/ko/mota-techlink/dh_pipeline">한국어</a> |   
  <a href="https://zdoc.app/ja/mota-techlink/dh_pipeline">日本語</a> |     
</div>

<br/>

> The value of this project:
>
> Unlike standalone tools, dh_pipeline solves the version conflict between Torch 2.1.2 and MMCV, ensuring a one-click deployment experience. 
<br/>


## 1. Environment preparation

> It is strongly recommended to use conda
```bash
mkdir dh_pipeline
cd dh_pipeline
conda create -n dh_pipeline python=3.10 -y
conda activate dh_pipeline
```

## 2. Translation and voice generating
>Install Google Deep Translator and Microsoft EdgeTTS to translate content from the original language to another language, then generate sound accordingly.

```bash
pip install deep-translator edge-tts
```

>Run the translation and TTS gen
```bash
python run_tts.py
```

## 3. Video Combine
> Let static avator be moving along with the sample video that could be anyone's movement.

<p align="center">
  <img src="https://github.com/KlingTeam/LivePortrait/raw/main/assets/docs/showcase2.gif" alt="image">
</p>

### a. Get source of LivePortrait
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
  > You can check your CUDA version using `nvidia-smi`. If your CUDA version is 11.8 or higher, use the installation command for CUDA 11.8 or above, and always keep the torch version at 2.1.2 to avoid conflicts with MuseTalk.

  **Check Numpy, should not be greater than 2.0, if so downgrade**
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
> default saved result at LivePortrait/animations
```bash
 python inference.py
```

or with image and driving video path

```bash
python inference.py  --source "assets/examples/source/s12.jpg"   --driving "assets/examples/driving/d13.mp4" 
```

## 4. Mouth match

![Model Structure](https://github.com/user-attachments/assets/02f4a214-1bdd-4326-983c-e70b478accba)

## Cases

<table>
<tr>
<td width="33%">

### Input Video
---
https://github.com/TMElyralab/MuseTalk/assets/163980830/37a3a666-7b90-4244-8d3a-058cb0e44107

---
https://github.com/user-attachments/assets/1ce3e850-90ac-4a31-a45f-8dfa4f2960ac

---
https://github.com/user-attachments/assets/fa3b13a1-ae26-4d1d-899e-87435f8d22b3

---
https://github.com/user-attachments/assets/15800692-39d1-4f4c-99f2-aef044dc3251

---
https://github.com/user-attachments/assets/a843f9c9-136d-4ed4-9303-4a7269787a60

---
https://github.com/user-attachments/assets/6eb4e70e-9e19-48e9-85a9-bbfa589c5fcb

</td>
<td width="33%">

### MuseTalk 1.0
---
https://github.com/user-attachments/assets/c04f3cd5-9f77-40e9-aafd-61978380d0ef

---
https://github.com/user-attachments/assets/2051a388-1cef-4c1d-b2a2-3c1ceee5dc99

---
https://github.com/user-attachments/assets/b5f56f71-5cdc-4e2e-a519-454242000d32

---
https://github.com/user-attachments/assets/a5843835-04ab-4c31-989f-0995cfc22f34

---
https://github.com/user-attachments/assets/3dc7f1d7-8747-4733-bbdd-97874af0c028

---
https://github.com/user-attachments/assets/3c78064e-faad-4637-83ae-28452a22b09a

</td>
<td width="33%">

### MuseTalk 1.5
---
https://github.com/user-attachments/assets/999a6f5b-61dd-48e1-b902-bb3f9cbc7247

---
https://github.com/user-attachments/assets/d26a5c9a-003c-489d-a043-c9a331456e75

---
https://github.com/user-attachments/assets/471290d7-b157-4cf6-8a6d-7e899afa302c

---
https://github.com/user-attachments/assets/1ee77c4c-8c70-4add-b6db-583a12faa7dc

---
https://github.com/user-attachments/assets/370510ea-624c-43b7-bbb0-ab5333e0fcc4

---
https://github.com/user-attachments/assets/b011ece9-a332-4bc1-b8b7-ef6e383d7bde

</td>
</tr>
</table>

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

# make sure the version of mmcv is following:
wget https://download.openmmlab.com/mmcv/dist/cu118/torch2.1.0/mmcv-2.1.0-cp310-cp310-manylinux1_x86_64.whl

pip install mmcv-2.1.0-cp310-cp310-manylinux1_x86_64.whl

# Strictly limit the versions of the remaining dependencies
pip install "transformers==4.37.2" "diffusers==0.24.0" "accelerate==0.26.0" "huggingface-hub==0.23.5" "tokenizers==0.15.2" "opencv-python-headless==4.9.0.80" "omegaconf" "imageio-ffmpeg" "av" "scipy"

# Finally install OpenMMLab components
pip install "mmengine>=0.10.0" "mmpose>=1.1.0" "mmdet>=3.1.0"

# verify
python -c "import torch; import cv2; import numpy; from mmcv.ops import MultiScaleDeformableAttention; print(f'✅ Perfect enviroment: Torch={torch.__version__}, NumPy={numpy.__version__}, MMCV OK')"
```

> if it does not show ' ✅ Perfect enviroment: Torch=2.1.2+cu118, NumPy=1.26.4, MMCV O', please start over!!!

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


### d. Run the inference
```bash
sh inference.sh v1.5 realtime
```

## ❓ Frequently Asked Questions (FAQ)

**Q: Can this pipeline run on a consumer-grade GPU?**
A: Yes, it is optimized for NVIDIA GPUs with at least 8GB VRAM (e.g., RTX 3060 and above).

**Q: Does it support real-time generation?**
A: Currently, it supports high-speed offline inference. Real-time support is in the MOTA TECHLINK roadmap.

**Q: Why use Edge-TTS instead of other providers?**
A: Edge-TTS provides the best balance between natural prosody and zero-cost local integration.