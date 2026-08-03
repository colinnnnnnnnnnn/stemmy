class DbError(Exception):
    pass


class JobAlreadyExistsError(DbError):
    pass


class InvalidJobUpdateError(DbError):
    pass


class JobNotFoundError(DbError):
    pass
