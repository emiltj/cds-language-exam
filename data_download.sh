#! /bin/sh

# This script will download the required data from a google drive folder

# Install gdown
pip install gdown

# Install data

# Download data for assignment 3
cd assignment_3
mkdir data
cd data
printf "[INFO] Downloading data for assignment 3 ..."
gdown https://drive.google.com/uc?id=1tbJeaiTetkvhp8U0ca2smq7JBA0F5KV-
unzip a_million_news_headlines.zip
rm a_million_news_headlines.zip
printf "[INFO] The required data for assignment 3 has been downloaded successfully"

# Download data for assignment 4
cd ../../assignment_4
mkdir data
cd data
printf "\n\n[INFO] Downloading data for assignment 4 ...\n\n"
gdown https://drive.google.com/uc?id=1Zr4tpy-TrF3UGTq2ZnG1pHx5vOvmfAQ5
echo "[INFO] The required data for assignment 4 has been downloaded successfully"

# Download data for assignment 5
cd ../../assignment_5
mkdir data
cd data
printf "\n\n[INFO] Downloading data for assignment 5 ...\n\n"
gdown https://drive.google.com/uc?id=13H0U_PSxnh_zC0mWU-xQAsXZre2YXN8N 
unzip history_of_philosophy.zip
rm history_of_philosophy.zip
printf "[INFO] The required data for assignment 5 has been downloaded successfully"

# Download data for assignment 6
cd ../../assignment_6
mkdir data
cd data
printf "\n\n[INFO] Downloading data for assignment 6 ...\n\n"
gdown https://drive.google.com/uc?id=1hUEiG2yHMdRsnIH4HsiBxh2qrvqqeiP3
unzip game_of_thrones_script_all_seasons.zip
rm game_of_thrones_script_all_seasons.zip
mkdir glove
cd glove
gdown https://drive.google.com/uc?id=13fgtjW9pAwcYmY3CSme-Y2W4NwZniMuR
gdown https://drive.google.com/uc?id=1t-bb-bwh9BrnAcLBFngSVpcm-SI3VLVA
printf "[INFO] The required data for assignment 6 has been downloaded successfully"

# Download data for self-assigned
cd ../../../assignment_7
mkdir data
cd data
printf "\n\n[INFO] Downloading data for assignment_7 (self-assigned) ...\n\n"
gdown https://drive.google.com/uc?id=1_VMsre7E2PvBtuivCnvE0SHjkMAOqRMF
unzip archive.zip
rm archive.zip
printf "[INFO] The required data for assignment 7 has been downloaded successfully"
printf "\n\n[INFO] All data has been downloaded, script stopping"
cd ../..