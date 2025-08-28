from tasks import dedup_data_task, dedup_run_task, null_task, user_add_task, user_disable_task, user_reset_task, user_copycat_task, mat_validate_task

tasks = {
    "criar": user_add_task.execute,
    "resetar": user_reset_task.execute,
    "inativar": user_disable_task.execute,
    "espelhar": user_copycat_task.execute,
    "deduplicador_data": dedup_data_task.execute,
    "deduplicador_run": dedup_run_task.execute,
    "mat_validate": mat_validate_task.execute, 
}


def run_task(task_name, inputs):

    task = tasks.get(task_name)
    if task:
        task(inputs)
    else:
        null_task.execute()