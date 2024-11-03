# store/db_router.py
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """Направляем все запросы на чтение к реплике."""
        return 'replica'

    def db_for_write(self, model, **hints):
        """Направляем все запросы на запись к основной базе данных."""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Разрешаем отношения, если обе модели используют одну и ту же базу данных."""
        db_list = ('default', 'replica')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Определяем, разрешена ли миграция на определенной базе данных."""
        return db == 'default'
