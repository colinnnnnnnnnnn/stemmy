class DbError(Exception):
    pass


class JobAlreadyExistsError(DbError):
    pass


class InvalidJobUpdateError(DbError):
    pass


class JobNotFoundError(DbError):
    pass


class DownloadError(Exception):
    pass


class JobFailedError(Exception):
    pass
