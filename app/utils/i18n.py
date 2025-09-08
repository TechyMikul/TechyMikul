"""
Internationalization utilities for multi-language support
"""
from typing import Dict, Any
import json
import os


class I18nManager:
    """Internationalization manager for multi-language support"""
    
    def __init__(self, translations_dir: str = "app/translations"):
        self.translations_dir = translations_dir
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.load_translations()
    
    def load_translations(self) -> None:
        """Load translation files"""
        if not os.path.exists(self.translations_dir):
            os.makedirs(self.translations_dir, exist_ok=True)
            self._create_default_translations()
            return
        
        for filename in os.listdir(self.translations_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Remove .json extension
                file_path = os.path.join(self.translations_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
    
    def _create_default_translations(self) -> None:
        """Create default translation files"""
        default_translations = {
            "en": {
                "welcome": {
                    "title": "Welcome to EduOpportunity Bot!",
                    "description": "I'm here to help you discover amazing educational opportunities including:",
                    "features": [
                        "Scholarships",
                        "Free learning resources",
                        "Events and workshops",
                        "Mentorship programs",
                        "Funding opportunities"
                    ],
                    "get_started": "Use /register to get started and /help to see all available commands."
                },
                "help": {
                    "title": "Available Commands:",
                    "commands": {
                        "start": "Welcome message and main menu",
                        "register": "Register as a student",
                        "preferences": "Set your preferences",
                        "opportunities": "Browse available opportunities",
                        "subscribe": "Subscribe to an opportunity",
                        "unsubscribe": "Unsubscribe from an opportunity",
                        "help": "Show this help message"
                    },
                    "tips": "Set your preferences to get personalized recommendations"
                },
                "registration": {
                    "title": "Registration",
                    "description": "Let's get you registered! Please provide the following information:",
                    "fields": {
                        "email": "Email address",
                        "field": "Field of study",
                        "level": "Education level",
                        "interests": "Interests (comma-separated)"
                    },
                    "example": "Email: john@example.com\nField: Computer Science\nLevel: Undergraduate\nInterests: AI, Machine Learning, Web Development"
                },
                "preferences": {
                    "title": "Preferences Settings",
                    "description": "Set your preferences to get personalized opportunity recommendations:",
                    "fields": {
                        "interests": "What topics interest you?",
                        "education_level": "High School, Undergraduate, Graduate, etc.",
                        "field_of_study": "Your major or area of focus",
                        "location": "Your preferred location",
                        "notification_frequency": "How often to receive alerts"
                    }
                },
                "opportunities": {
                    "title": "Available Opportunities",
                    "no_opportunities": "No opportunities found matching your criteria.",
                    "subscribe_instruction": "Use /subscribe <number> to subscribe to an opportunity."
                },
                "subscription": {
                    "success": "Successfully subscribed to opportunity",
                    "unsubscribed": "Unsubscribed from opportunity",
                    "not_found": "Opportunity not found",
                    "already_subscribed": "You are already subscribed to this opportunity"
                },
                "errors": {
                    "general": "I'm here to help you find educational opportunities!",
                    "invalid_command": "Invalid command. Use /help to see available commands.",
                    "user_not_found": "User not found. Please register first.",
                    "opportunity_not_found": "Opportunity not found.",
                    "subscription_failed": "Failed to create subscription."
                }
            },
            "es": {
                "welcome": {
                    "title": "¡Bienvenido al Bot de Oportunidades Educativas!",
                    "description": "Estoy aquí para ayudarte a descubrir increíbles oportunidades educativas incluyendo:",
                    "features": [
                        "Becas",
                        "Recursos de aprendizaje gratuitos",
                        "Eventos y talleres",
                        "Programas de mentoría",
                        "Oportunidades de financiamiento"
                    ],
                    "get_started": "Usa /registro para comenzar y /ayuda para ver todos los comandos disponibles."
                },
                "help": {
                    "title": "Comandos Disponibles:",
                    "commands": {
                        "start": "Mensaje de bienvenida y menú principal",
                        "register": "Registrarse como estudiante",
                        "preferences": "Configurar preferencias",
                        "opportunities": "Explorar oportunidades disponibles",
                        "subscribe": "Suscribirse a una oportunidad",
                        "unsubscribe": "Cancelar suscripción a una oportunidad",
                        "help": "Mostrar este mensaje de ayuda"
                    },
                    "tips": "Configura tus preferencias para obtener recomendaciones personalizadas"
                },
                "registration": {
                    "title": "Registro",
                    "description": "¡Registrémonos! Por favor proporciona la siguiente información:",
                    "fields": {
                        "email": "Dirección de correo electrónico",
                        "field": "Campo de estudio",
                        "level": "Nivel educativo",
                        "interests": "Intereses (separados por comas)"
                    },
                    "example": "Email: juan@ejemplo.com\nCampo: Ciencias de la Computación\nNivel: Pregrado\nIntereses: IA, Aprendizaje Automático, Desarrollo Web"
                },
                "preferences": {
                    "title": "Configuración de Preferencias",
                    "description": "Configura tus preferencias para obtener recomendaciones personalizadas de oportunidades:",
                    "fields": {
                        "interests": "¿Qué temas te interesan?",
                        "education_level": "Bachillerato, Pregrado, Posgrado, etc.",
                        "field_of_study": "Tu especialización o área de enfoque",
                        "location": "Tu ubicación preferida",
                        "notification_frequency": "Con qué frecuencia recibir alertas"
                    }
                },
                "opportunities": {
                    "title": "Oportunidades Disponibles",
                    "no_opportunities": "No se encontraron oportunidades que coincidan con tus criterios.",
                    "subscribe_instruction": "Usa /suscribir <número> para suscribirte a una oportunidad."
                },
                "subscription": {
                    "success": "Te has suscrito exitosamente a la oportunidad",
                    "unsubscribed": "Te has desuscrito de la oportunidad",
                    "not_found": "Oportunidad no encontrada",
                    "already_subscribed": "Ya estás suscrito a esta oportunidad"
                },
                "errors": {
                    "general": "¡Estoy aquí para ayudarte a encontrar oportunidades educativas!",
                    "invalid_command": "Comando inválido. Usa /ayuda para ver los comandos disponibles.",
                    "user_not_found": "Usuario no encontrado. Por favor regístrate primero.",
                    "opportunity_not_found": "Oportunidad no encontrada.",
                    "subscription_failed": "Error al crear la suscripción."
                }
            },
            "fr": {
                "welcome": {
                    "title": "Bienvenue sur le Bot d'Opportunités Éducatives !",
                    "description": "Je suis là pour vous aider à découvrir d'incroyables opportunités éducatives incluant :",
                    "features": [
                        "Bourses d'études",
                        "Ressources d'apprentissage gratuites",
                        "Événements et ateliers",
                        "Programmes de mentorat",
                        "Opportunités de financement"
                    ],
                    "get_started": "Utilisez /inscription pour commencer et /aide pour voir toutes les commandes disponibles."
                },
                "help": {
                    "title": "Commandes Disponibles :",
                    "commands": {
                        "start": "Message de bienvenue et menu principal",
                        "register": "S'inscrire en tant qu'étudiant",
                        "preferences": "Définir vos préférences",
                        "opportunities": "Parcourir les opportunités disponibles",
                        "subscribe": "S'abonner à une opportunité",
                        "unsubscribe": "Se désabonner d'une opportunité",
                        "help": "Afficher ce message d'aide"
                    },
                    "tips": "Définissez vos préférences pour obtenir des recommandations personnalisées"
                },
                "registration": {
                    "title": "Inscription",
                    "description": "Inscrivons-nous ! Veuillez fournir les informations suivantes :",
                    "fields": {
                        "email": "Adresse e-mail",
                        "field": "Domaine d'études",
                        "level": "Niveau d'éducation",
                        "interests": "Intérêts (séparés par des virgules)"
                    },
                    "example": "Email: jean@exemple.com\nDomaine: Informatique\nNiveau: Licence\nIntérêts: IA, Apprentissage Automatique, Développement Web"
                },
                "preferences": {
                    "title": "Paramètres des Préférences",
                    "description": "Définissez vos préférences pour obtenir des recommandations personnalisées d'opportunités :",
                    "fields": {
                        "interests": "Quels sujets vous intéressent ?",
                        "education_level": "Lycée, Licence, Master, etc.",
                        "field_of_study": "Votre spécialisation ou domaine d'étude",
                        "location": "Votre localisation préférée",
                        "notification_frequency": "Fréquence des notifications"
                    }
                },
                "opportunities": {
                    "title": "Opportunités Disponibles",
                    "no_opportunities": "Aucune opportunité trouvée correspondant à vos critères.",
                    "subscribe_instruction": "Utilisez /souscrire <numéro> pour vous abonner à une opportunité."
                },
                "subscription": {
                    "success": "Abonnement réussi à l'opportunité",
                    "unsubscribed": "Désabonné de l'opportunité",
                    "not_found": "Opportunité non trouvée",
                    "already_subscribed": "Vous êtes déjà abonné à cette opportunité"
                },
                "errors": {
                    "general": "Je suis là pour vous aider à trouver des opportunités éducatives !",
                    "invalid_command": "Commande invalide. Utilisez /aide pour voir les commandes disponibles.",
                    "user_not_found": "Utilisateur non trouvé. Veuillez vous inscrire d'abord.",
                    "opportunity_not_found": "Opportunité non trouvée.",
                    "subscription_failed": "Échec de la création de l'abonnement."
                }
            }
        }
        
        for lang_code, translations in default_translations.items():
            file_path = os.path.join(self.translations_dir, f"{lang_code}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
        
        self.load_translations()
    
    def get_text(self, key: str, lang: str = "en", **kwargs) -> str:
        """Get translated text by key"""
        try:
            # Split key by dots to navigate nested structure
            keys = key.split('.')
            text = self.translations.get(lang, self.translations.get("en", {}))
            
            for k in keys:
                text = text[k]
            
            # Format with kwargs if provided
            if isinstance(text, str) and kwargs:
                return text.format(**kwargs)
            elif isinstance(text, list):
                return "\n".join(text)
            else:
                return str(text)
        except (KeyError, TypeError):
            # Fallback to English if translation not found
            if lang != "en":
                return self.get_text(key, "en", **kwargs)
            return key  # Return key if no translation found
    
    def get_opportunity_message(self, opportunity: Dict[str, Any], lang: str = "en") -> str:
        """Get formatted opportunity message in specified language"""
        message = f"🎓 *{opportunity['title']}*\n\n"
        message += f"📝 {opportunity['description'][:200]}...\n\n"
        message += f"🏢 {self.get_text('opportunities.organization', lang)}: {opportunity['organization']}\n"
        
        if opportunity.get('deadline'):
            message += f"⏰ {self.get_text('opportunities.deadline', lang)}: {opportunity['deadline']}\n"
        
        if opportunity.get('location'):
            message += f"📍 {self.get_text('opportunities.location', lang)}: {opportunity['location']}\n"
        
        if opportunity.get('url'):
            message += f"🔗 {self.get_text('opportunities.learn_more', lang)}: {opportunity['url']}\n"
        
        if opportunity.get('tags'):
            tags = ", ".join(opportunity['tags'][:5])
            message += f"🏷️ {self.get_text('opportunities.tags', lang)}: {tags}\n"
        
        return message


# Global instance
i18n = I18nManager()