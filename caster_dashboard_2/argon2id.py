from django.contrib.auth.hashers import *
from django.utils.translation import gettext_noop as _


class Argon2idPasswordHasher(Argon2PasswordHasher):
    """
        Use the newer argon2id algorithm until release of django 3.2
        Taken from github
        https://github.com/django/django/pull/13066/files
    """

    """
       Secure password hashing using the argon2 algorithm.
       This is the winner of the Password Hashing Competition 2013-2015
       (https://password-hashing.net). It requires the argon2-cffi library which
       depends on native C code and might cause portability issues.
       """
    algorithm = 'argon2'
    library = 'argon2'

    time_cost = 2
    memory_cost = 102400
    parallelism = 8

    def encode(self, password, salt):
        argon2 = self._load_library()
        params = self.params()
        data = argon2.low_level.hash_secret(
            password.encode(),
            salt.encode(),
            time_cost=params.time_cost,
            memory_cost=params.memory_cost,
            parallelism=params.parallelism,
            hash_len=params.hash_len,
            type=params.type,
        )
        return self.algorithm + data.decode('ascii')

    def verify(self, password, encoded):
        argon2 = self._load_library()
        algorithm, rest = encoded.split('$', 1)
        assert algorithm == self.algorithm
        try:
            return argon2.PasswordHasher().verify('$' + rest, password)
        except argon2.exceptions.VerificationError:
            return False

    def safe_summary(self, encoded):
        (algorithm, variety, version, time_cost, memory_cost, parallelism,
         salt, data) = self._decode(encoded)
        assert algorithm == self.algorithm
        return {
            _('algorithm'): algorithm,
            _('variety'): variety,
            _('version'): version,
            _('memory cost'): memory_cost,
            _('time cost'): time_cost,
            _('parallelism'): parallelism,
            _('salt'): mask_hash(salt),
            _('hash'): mask_hash(data),
        }

    def must_update(self, encoded):
        algorithm, rest = encoded.split('$', 1)
        assert algorithm == self.algorithm
        argon2 = self._load_library()
        current_params = argon2.extract_parameters('$' + rest)
        new_params = self.params()
        # Set salt_len to the salt_len of the current parameters because salt
        # is explicitly passed to argon2.
        new_params.salt_len = current_params.salt_len
        return current_params != new_params

    def harden_runtime(self, password, encoded):
        # The runtime for Argon2 is too complicated to implement a sensible
        # hardening algorithm.
        pass

    def params(self):
        argon2 = self._load_library()
        # salt_len is a noop, because we provide our own salt.
        return argon2.Parameters(
            type=argon2.low_level.Type.ID,
            version=argon2.low_level.ARGON2_VERSION,
            salt_len=argon2.DEFAULT_RANDOM_SALT_LENGTH,
            hash_len=argon2.DEFAULT_HASH_LENGTH,
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
        )

    def _decode(self, encoded):
        """
        Split an encoded hash and return: (
            algorithm, variety, version, time_cost, memory_cost,
            parallelism, salt, data,
        ).
        """
        argon2 = self._load_library()
        algorithm, rest = encoded.split('$', 1)
        params = argon2.extract_parameters('$' + rest)
        variety, *_, salt, data = rest.split('$')
        return (
            algorithm, variety, params.version, params.time_cost,
            params.memory_cost, params.parallelism, salt, data,
        )
