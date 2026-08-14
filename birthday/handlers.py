"""post_migrate handling for birthday.fields.BirthdayField."""

from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS
from django.db import router

BATCH_SIZE = 500


def handle_post_migrate(
    app_config,
    *,
    interactive=True,
    using=DEFAULT_DB_ALIAS,
    apps=global_apps,
    **kwargs,
):
    try:
        app_config = apps.get_app_config(app_config.label)
    except LookupError:
        return

    # Some post_migrate senders (e.g. Django's internal AppConfigStub, used
    # when building the test database or running `migrate --run-syncdb` for
    # apps without a migrations/ directory -- which includes this app) never
    # set models_module at all, rather than leaving it None.
    if not getattr(app_config, "models_module", None):
        return

    for model in app_config.get_models():
        if not hasattr(model._meta, "birthday_field"):  # noqa: SLF001
            continue

        if not router.allow_migrate_model(using, model):
            continue

        field_obj = model._meta.birthday_field  # noqa: SLF001
        name, doy_name = field_obj.name, field_obj.doy_name

        queryset = (
            model._base_manager.using(using)  # noqa: SLF001
            .filter(**{f"{doy_name}__isnull": True, f"{name}__isnull": False})
            .only("pk", name, doy_name)
            .iterator(chunk_size=BATCH_SIZE)
        )

        batch = []
        for instance in queryset:
            setattr(instance, doy_name, getattr(instance, name).timetuple().tm_yday)
            batch.append(instance)
            if len(batch) >= BATCH_SIZE:
                model._base_manager.using(using).bulk_update(  # noqa: SLF001
                    batch,
                    [doy_name],
                    batch_size=BATCH_SIZE,
                )
                batch = []

        if batch:
            model._base_manager.using(using).bulk_update(  # noqa: SLF001
                batch,
                [doy_name],
                batch_size=BATCH_SIZE,
            )
