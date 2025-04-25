import mysql.connector
from collections import defaultdict, deque
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MigrationManager:
    def __init__(self, host, user, password, database, project_path):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.project_path = project_path
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            logging.info("Successfully connected to the database.")
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            self.connection = None
            self.cursor = None

    def close_database(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            logging.info("Database connection closed.")

    def get_table_dependencies(self):
        try:
            self.cursor.execute(f"""
                SELECT TABLE_NAME, REFERENCED_TABLE_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE REFERENCED_TABLE_NAME IS NOT NULL
                AND TABLE_SCHEMA = '{self.database}';
            """)

            dependencies = defaultdict(list)
            for row in self.cursor.fetchall():
                table_name = row[0]
                referenced_table_name = row[1]
                dependencies[referenced_table_name].append(table_name)

            self.cursor.execute(f"""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = '{self.database}';
            """)
            all_tables = {row[0] for row in self.cursor.fetchall()}

            for table in all_tables:
                if table not in dependencies:
                    dependencies[table] = []

            logging.info(f"Dependencies: {dependencies}")
            return dependencies
        except mysql.connector.Error as err:
            logging.error(f"Error retrieving table dependencies: {err}")
            return None

    def topological_sort(self, dependencies):
        try:
            indegree = defaultdict(int)
            for table in dependencies:
                for dependent_table in dependencies[table]:
                    indegree[dependent_table] += 1

            queue = deque([table for table in dependencies if indegree[table] == 0])
            sorted_tables = []

            while queue:
                table = queue.popleft()
                sorted_tables.append(table)
                for dependent_table in dependencies[table]:
                    indegree[dependent_table] -= 1
                    if indegree[dependent_table] == 0:
                        queue.append(dependent_table)

            if len(sorted_tables) != len(dependencies):
                raise Exception("Circular dependency detected or some tables are missing.")

            logging.info(f"Topological sorting completed: {sorted_tables}")
            return sorted_tables
        except Exception as err:
            logging.error(f"Error during topological sorting: {err}")
            return []

    def generate_migrations(self, sorted_tables):
        try:
            for table in sorted_tables:
                timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
                filename = f"{timestamp}_create_{table}_table.php"
                migration_command = f"php artisan migrate:generate --tables='{table}' --squash --table-filename='{filename}' --skip-log"
                os.system(f"cd {self.project_path} && {migration_command}")
                logging.info(f"Migration generated for table: {table}")
        except Exception as err:
            logging.error(f"Error generating migration: {err}")

    def write_to_file(self, sorted_tables, dependencies, output_log_file):
        try:
            with open(output_log_file, 'w') as file:
                file.write("Sorted Tables:\n")
                for table in sorted_tables:
                    file.write(f"{table}\n")

                file.write("\nDependencies:\n")
                for table, deps in dependencies.items():
                    file.write(f"{table} -> {deps}\n")

            logging.info(f"Sorted tables and dependencies written to {output_log_file}.")
        except Exception as err:
            logging.error(f"Error writing to file: {err}")

    def run(self):
        try:
            self.connect_to_database()
            if self.cursor is None:
                raise Exception("Failed to connect to the database.")

            dependencies = self.get_table_dependencies()
            if dependencies is None:
                raise Exception("Failed to retrieve table dependencies.")

            sorted_tables = self.topological_sort(dependencies)
            if not sorted_tables:
                raise Exception("Failed to sort tables. Check for circular dependencies or missing tables.")

            self.generate_migrations(sorted_tables)
            self.write_to_file(sorted_tables, dependencies, self.project_path+"/MigrationManagerLog.txt")
        except Exception as err:
            logging.error(f"Script terminated with an error: {err}")

        finally:
            self.close_database()

if __name__ == "__main__":
    migration_manager = MigrationManager(
        host='localhost',
        user='root',
        password='password',
        database='sutanu',
        project_path='/var/www/html/sutanu/bookingsystem-new'
    )
    migration_manager.run()
