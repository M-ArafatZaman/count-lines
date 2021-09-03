import os 

class Source:
    def __init__(self, source_dir):
        # Check if source exists
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"\"{source_dir}\" doesn't exist")

        # Store the source directory or file
        self.source_dir = source_dir
        self._ignore_name = ["__pycache__"] # Directories of file to ignore
        self._ignore_absolute_path = [] # Absolute path to ignore

    # Ignore name
    def ignore(self, name):
        self._ignore_name.append(name)

    # Ignore path
    def ignore_absolute_path(self, path):
        self._ignore_absolute_path.append(path)

    # Check whether to ignore the file or directory 
    def willIgnorePath(self, name, curr_path):
        ignore_file_or_directory = False
        
        # Check ignore names
        for name_to_ignore in self._ignore_name:
            if name == name_to_ignore:
                ignore_file_or_directory = True
                break
        
        # Check ignore paths
        if not ignore_file_or_directory:
            for path_to_ignore in self._ignore_absolute_path:
                if os.path.normpath(path_to_ignore) == curr_path:
                    ignore_file_or_directory = True
                    break
        
        return ignore_file_or_directory

    # Count lines
    def count_lines(self):
        count = self.count_lines_dir(self.source_dir)
        return count

    
    # Count lines in a directory
    def count_lines_dir(self, path):
        # Check if the path is a directory
        if not os.path.isdir(path):
            raise FileNotFoundError(f"'{path}' is not a valid directory.")
    
        count = 0

        # Iterate through each file/directories in source
        for file_or_directory in os.listdir(path):
            current_path = os.path.join(path, file_or_directory)

            # If file or directory is to be ignored, continue to the next
            ignore_file_or_directory = self.willIgnorePath(file_or_directory, current_path)
            
            # Continue if the file or directory is to be ignore
            if ignore_file_or_directory:
                print(f"Ignored: '{current_path}'")
                continue
            else:
                # If the path is a file
                if os.path.isfile(current_path):
                    count += self.count_lines_file(current_path)
                
                # Else if the path is a directory
                elif os.path.isdir(current_path):
                    count += self.count_lines_dir(current_path)

        return count
        
    
    # Count lines in a file
    def count_lines_file(self, path):
        # Check if the path is a file
        if not os.path.isfile(path):
            raise FileNotFoundError(f"'{path}' is not a valid file.")
        
        count = 0

        # Try counting the lines
        try:
            with open(path, "r") as file_to_count:
                for l in file_to_count:
                    count += 1

            count += 1

            print(f"'{path}' => {count} lines")
        except UnicodeDecodeError:
            print(f"Ignored: '{path}'")
            count = 0

        return count


if __name__ == "__main__":

    # Enter the directory of the source code folder
    """ 
    This project was initially created to help count my website's code which was made using django
    """
    counter = Source("TestDir")
    counter.ignore("migrations")
    counter.ignore("__init__.py")
    counter.ignore("superuser.txt")
    counter.ignore("db.sqlite3")
    counter.ignore_absolute_path("backend/")
    counter.ignore_absolute_path("manage.py/")
    counter.ignore_absolute_path("pages/static/assets/svg/")

    print(f"Total lines of code => {counter.count_lines()}")