# %%
import os
import re
import spacy



# %%
# Obtenir le chemin absolu du répertoire courant
current_directory = os.getcwd()

# Nom du fichier texte
transcription_filename = "transcription.txt"
stopwords_ca_filename = "stopwords-ca.txt"
stopwords_es_filename = "stopwords-es.txt"


# Chemin complet du fichier texte
transcription_filepath = os.path.join(current_directory, transcription_filename)
stopwords_filepath_ca = os.path.join(current_directory, stopwords_ca_filename)
stopwords_filepath_es = os.path.join(current_directory, stopwords_es_filename)

# %%
#vérifier si le fichier "transcription.txt" existe
if os.path.exists(transcription_filepath):
    # Chargement du texte de la transcription
    with open(transcription_filepath, encoding="utf-8") as file:
        full_text = file.read()

    if full_text:
        # Chargement du texte des stopwords ca
        with open(stopwords_filepath_ca, encoding="utf-8") as file:
            stopwords_text_ca = file.read()

        # Chargement du texte des stopwords es
        with open(stopwords_filepath_es, encoding="utf-8") as file:
            stopwords_text_es = file.read()  

        stopwords_text = stopwords_text_ca + stopwords_text_es
        stopwords_text+="s d l r o m e"

        # On supprime les sauts de ligne et rassemble les lignes en une seule chaîne
        texte = re.sub(r'\n', ' ', full_text)

        # On rassemble les mots séparés par des tirets en une seule partie
        texte = re.sub(r'(?<=[a-zA-Z])- ', '', texte) 
        texte = re.sub(r'(?<=[a-zA-Z])-', '', texte) 

        # Utiliser une expression régulière pour détacher les mots des symboles de ponctuation
        texte = re.sub(r'(\w)([^\w\s]+)(\w)', r'\1 \2 \3', texte)

        # Mettre en minuscule
        texte = texte.lower()
            
        # On sépare le texte en phrases contenues dans une liste
        phrases = re.findall(r'[^.!?]+[.!?]', texte)
            
        # Suppression des stopwords dans le corpus
        swlines = stopwords_text.split('\n')
        filtered_phrases_lemmatized = []

        #Charger un modèle catalan
        nlp_ca = spacy.load("ca_core_news_sm")

        # Suppression des stopwords et lemmatisation des phrases
        for phrase in phrases:
            doc = nlp_ca(phrase)
            lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_digit]
            filtered_tokens = [token.strip() for token in lemmatized_tokens if token.strip() and token not in stopwords_text.split()]
            filtered_phrases_lemmatized.append(filtered_tokens)

        # On retire l'espace de la liste des mots
        filtered_phrases_lemmatized = [[mot for mot in phrase if mot != ' '] for phrase in filtered_phrases_lemmatized]

        #print(filtered_phrases_lemmatized)
        
        # Chemin du fichier de sortie
        output_filepath = os.path.join(current_directory, "datalac_nettoye.txt")

        # Ouverture du fichier de sortie en mode écriture
        with open(output_filepath, "w", encoding="utf-8") as file:
            # Écriture de chaque phrase dans le fichier
            for phrase in filtered_phrases_lemmatized:
                # Convertir la liste de mots en une chaîne de caractères
                phrase_str = " ".join(phrase)
                # Écrire la phrase dans le fichier
                file.write(phrase_str + "\n")
        
        print('Success, You can now access the preprocessed version of your transcription : datalac_nettoye.txt')
    else : 
        print("Error, The text was not loaded correctly, please check the content of your transcription.txt file.")
else : 
    print("Error, The expected file 'transcription.txt' is not present in the folder or is not named in this way.")



# %%
