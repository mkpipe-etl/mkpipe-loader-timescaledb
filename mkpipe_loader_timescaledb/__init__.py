from mkpipe.spark import JdbcLoader

JAR_PACKAGES = ['org.postgresql:postgresql:42.7.4']


class TimescaleDBLoader(JdbcLoader, variant='timescaledb'):
    driver_name = 'postgresql'
    driver_jdbc = 'org.postgresql.Driver'
    _dialect = 'timescaledb'

    def build_jdbc_url(self):
        url = (
            f'jdbc:{self.driver_name}://{self.host}:{self.port}/{self.database}'
            f'?user={self.username}&password={self.password}'
        )
        if self.schema:
            url += f'&currentSchema={self.schema}'
        return url
