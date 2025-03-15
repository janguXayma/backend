from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    logger.info("Tâche exécutée avec succès")
    print("La tâche add a été exécutée")
    return x + y
