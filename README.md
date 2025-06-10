# Chronos - Time Tracking Application

Une application minimaliste de suivi du temps et de gestion des tâches, conçue pour un usage personnel avec export vers ERP.

## Description

Chronos est une application de bureau légère développée en Python qui permet de suivre facilement le temps passé sur différentes tâches au cours d'une journée de travail. Elle a été conçue avec une interface simple et efficace pour minimiser les frictions lors de la saisie des temps.

## Fonctionnalités

- ⏰ Gestion des journées de travail (début/fin)
- ✍️ Création et suivi des tâches
- ⌛️ Chronométrage automatique du temps par tâche
- 📊 Export des données au format CSV pour intégration ERP
- 📋 Visualisation de l'historique des tâches

## Installation

L'application est distribuée sous forme de package exécutable via PyInstaller :

### macOS (ARM64)
- Téléchargez la dernière version de Chronos pour macOS ARM64
- Décompressez l'archive
- Déplacez l'application dans votre dossier Applications
- Double-cliquez sur l'application pour la lancer

*Note: Les versions pour d'autres systèmes d'exploitation et architectures seront disponibles prochainement.*

## Utilisation

1. Lancez l'application Chronos
2. Cliquez sur "Commencer la journée" pour démarrer une session
3. Saisissez le nom de votre tâche dans le champ prévu
4. Utilisez les boutons "Commencer" et "Terminer" pour chronométrer vos tâches
5. Consultez la liste des tâches via le bouton dédié
6. Terminez votre journée avec le bouton "Terminer la journée"

Les données sont automatiquement sauvegardées dans un fichier CSV pour une intégration ultérieure dans votre ERP.

## Développement

### Prérequis
- Python 3.13+
- tkinter (inclus dans la distribution Python standard)
- PyInstaller (pour la création des exécutables)

### Structure du projet
```
chronos/
├── main.py              # Point d'entrée de l'application
├── modules/            # Modules principaux
│   ├── app.py         # Interface utilisateur principale
│   ├── csveditor.py   # Visualisateur de tâches
│   └── taskmanager.py # Gestion des tâches
├── utils/             # Utilitaires
│   ├── config.py      # Gestion de la configuration
│   └── logger.py      # Configuration des logs
└── assets/            # Ressources graphiques
```

## Roadmap

### Prochaines fonctionnalités
- [ ] Intégration des fonctionnalités CRUD dans le visualisateur de tâches
- [ ] Support pour Windows et Linux
- [ ] Support pour les architectures x86_64

## Licence

Ce projet est sous licence GPL-3.0 - voir le fichier `LICENSE` pour plus de détails.
