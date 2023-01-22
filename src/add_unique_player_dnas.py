import glob
from math import ceil
import re
from utils import load_file_into_string, write_to_file
import rubicon_parser as paradox

gene_genders = [ 'male', 'female']
# Determine unique skin gene value
unique_player_skin_value = {}
for gene_gender in gene_genders:
    unique_players = paradox.loads("common/genes/95_genes_portrait2d.txt")['accessory_genes']['base_skins']['gene_unique_skin'][gene_gender]['1']
    total_players = len(unique_players)
    for i, unique_player in enumerate(unique_players):
        unique_player_skin_value[unique_player.lower()] = ceil((i/total_players)*255)

# Load all files in dna_data folder and update them
for player, unique_skin_value in unique_player_skin_value.items():
    string = f"""dna_{player} = {{
    portrait_info = {{
        genes = {{         
            hair_color={{ 0 0 0 0 }}
            skin_color={{ 0 0 0 0 }}
            eye_color={{ 0 0 0 0 }}
            gene_complexion={{ "complexion_01" 127 "complexion_01" 127 }}
            gene_stubble={{ "stubble_low" 127 "stubble_low" 127 }}
            gene_face_dacals={{ "face_dacal_01" 127 "face_dacal_01" 127 }}
            gene_eyebrows_shape={{ "no_eyebrows" 127 "no_eyebrows" 127 }}
            gene_eyebrows_fullness={{ "no_eyebrows" 127 "no_eyebrows" 127 }}
            hairstyles={{ "no_hairstyles" 0 "no_hairstyles" 0 }}
            beards={{ "all_beards" 0 "all_beards" 0 }}
            props={{ "no_prop" 0 "no_prop" 0 }}
            eye_accessory={{ "normal_eyes" 0 "normal_eyes" 0 }}
            eye_lashes_accessory={{ "normal_eyelashes" 0 "normal_eyelashes" 0 }}
            teeth_accessory={{ "normal_teeth" 0 "normal_teeth" 0 }}
            gene_no_portrait={{ "no_portrait" 127 "no_portrait" 127 }}
            base_skins={{ "gene_unique_skin" {unique_skin_value} "gene_base_skin" 0 }}
        }}
    }}
    enabled = yes
}}"""
    write_to_file(f"common/dna_data/00_{player}.txt", string)
