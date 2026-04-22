class AureliumError(Exception):
    pass


class ValidationError(AureliumError):
    pass


class ProviderUnavailableError(AureliumError):
    pass
