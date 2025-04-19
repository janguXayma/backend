from django.db import models

# Create your models here.

# mon_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cryptography.fernet import Fernet
import os
import datetime
import base64
import PyPDF2  # Bibliothèque pour extraire du texte d'un PDF




# Générer une clé de chiffrement unique (stocke-la en sécurité)
# ENCRYPTION_KEY = b'H7Ldxi1BAUqVufd3u3EzZmBjlimZu3Z-JqsOoM6IhNo='  # Remplace ceci par une clé sécurisée
# cipher = Fernet(ENCRYPTION_KEY)


def simple_encrypt(text, key=42):
    """Chiffre avec XOR + encodage base64 URL-safe"""
    encrypted_bytes = bytes([ord(char) ^ key for char in text])
    encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes).decode()
    return encrypted_b64.rstrip('=')  # Supprime le padding pour la compatibilité 

def simple_decrypt(encrypted_text, key=42):
    """Déchiffre le base64 URL-safe + XOR"""
    try:
        # Réajoute le padding si nécessaire
        encrypted_text += '=' * ((4 - len(encrypted_text) % 4) % 4)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_text)
        return ''.join([chr(byte ^ key) for byte in encrypted_bytes])
    except Exception as e:
        return f"Erreur : {str(e)}"

def encrypt_text(text):
    """Chiffre un texte avec une méthode simple XOR."""
    return simple_encrypt(text)

def decrypt_text(encrypted_text):
    """Déchiffre un texte chiffré avec XOR."""
    return simple_decrypt(encrypted_text)


def upload_pdf_path(instance, filename):
    """ Génère un nom de fichier chiffré sécurisé """
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    original_name = f"{instance.user.username}.{date_str}"
    
    encrypted_name = encrypt_text(original_name)  # Utilise le nouveau chiffrement
    return f'pdf_uploads/{instance.user.username}/{encrypted_name}.pdf'

class Reponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to=upload_pdf_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Affiche le chemin final du fichier avant enregistrement"""
        super().save(*args, **kwargs)
        #pdf_uploads/username/fichier.pdf 
        print(f"Fichier enregistré sous : {self.pdf_file.name}")

    ##Fonction qui permet de recuperer le fichier chiffrer Stocke en base
    def get_encrypted_pdf(self):
        """
        Récupère le contenu  du fichier PDF avec nom chiffré depuis la base de données.
        """
        if not self.pdf_file:
            return None  # Aucun fichier enregistré

        try:
            with self.pdf_file.open('rb') as file:
                encrypted_content = file.read()  # Lire le contenu binaire du fichier
            return encrypted_content
        except Exception as e:
            return f"Erreur lors de la récupération du fichier : {str(e)}"

    ##Fonction qui permet de dechifer le nom du PDF Stocker en base
    def get_decrypted_pdf_name(self):
        """Déchiffre correctement le nom du fichier et retrouve le nom original."""
        if self.pdf_file and isinstance(self.pdf_file.name, str):
            # Récupérer uniquement le nom du fichier sans le chemin complet
            encrypted_filename = os.path.basename(self.pdf_file.name)
            
            # Supprimer l'extension `.pdf` si présente
            if encrypted_filename.endswith('.pdf'):
                encrypted_filename = encrypted_filename[:-4]

            try:
                decrypted_filename = decrypt_text(encrypted_filename)  # Déchiffrement sécurisé
                return f"{decrypted_filename}.pdf"  # Ajout de l'extension correcte
            except Exception as e:
                return f"Erreur de déchiffrement : {str(e)}"
        
        return None
        
        
    def delete_pdf(self):
        """
        Supprime physiquement le fichier PDF du stockage et met à jour la base de données.
        """
        if self.pdf_file:
            pdf_path = self.pdf_file.path  # Récupère le chemin physique du fichier
            
            # Vérifie si le fichier existe avant de le supprimer
            if os.path.exists(pdf_path):
                os.remove(pdf_path)  # Supprime le fichier du disque
                
        # Supprime l'objet de la base de données
        self.delete()

        return True 



    def pdf_to_text(self):
        """Déchiffre le fichier PDF, extrait son contenu texte et sauvegarde un fichier .txt"""
        if not self.pdf_file or not isinstance(self.pdf_file.name, str):
            return None

        encrypted_filename = os.path.basename(self.pdf_file.name).replace('.pdf', '')
        decrypted_filename = decrypt_text(encrypted_filename)

        try:
            encrypted_pdf_path = os.path.join(
                settings.MEDIA_ROOT, 'pdf_uploads', self.user.username, f"{encrypted_filename}.pdf"
            )

            if not os.path.exists(encrypted_pdf_path):
                print("Fichier PDF introuvable.")
                return None

            # Lire et extraire le texte
            text_content = []
            with open(encrypted_pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text_content.append(extracted_text)

            extracted_text = "\n".join(text_content) if text_content else None
            if not extracted_text:
                print("Aucun texte extrait.")
                return None

            # Dossier de sortie
            txt_output_dir = os.path.join(settings.MEDIA_ROOT, 'txt_outputs', self.user.username)
            os.makedirs(txt_output_dir, exist_ok=True)

            txt_output_path = os.path.join(txt_output_dir, f"{decrypted_filename}_extracted.txt")

            with open(txt_output_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(extracted_text)

            return txt_output_path

        except Exception as e:
            print(f"Erreur lors de l'extraction : {str(e)}")
            return None

    def __str__(self):
        # On peut afficher le chemin chiffré ou, pour le debug, le chemin déchiffré
        return f"{self.user.username} - {self.get_decrypted_path() or 'Fichier non disponible'}"
