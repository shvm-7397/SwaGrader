from swagrader.settings import BASE_DIR
import subprocess
import os

submissions_dir = "submissions"
test_data_dir = "TestData"


class Program:
    """ Class to Represent a program with its associated test files, user output file and running, compiling methods """
    def __init__(self, src_path, input_file, output_file, log_file, user_output, lang, prob_code):
        self.source_path = src_path
        self.input_path = input_file
        self.output_path = output_file
        self.log_path = log_file
        self.user_output_path = user_output
        self.language = lang
        self.problem_code = prob_code
        self.prob_wd = os.path.join(BASE_DIR, os.path.join(test_data_dir, self.problem_code))

    def compile(self):
        cmd, compile_status = "", 'Compiled'
        log_file = open(self.log_path, 'w')

        if self.language == 'cpp14':
            cmd += "g++ " + self.source_path + " -std=c++14"

        elif self.language == 'cpp':
            cmd += "g++ " + self.source_path

        elif self.language == 'c':
            cmd += "gcc " + self.source_path

        try:
            subprocess.check_call(cmd, shell=True, stderr=log_file, cwd=self.prob_wd)
        except subprocess.CalledProcessError:
            compile_status = 'Failed'
        log_file.close()
        if os.getcwd() == self.prob_wd:
            os.chdir(BASE_DIR)
        if compile_status == 'Failed':
            return False
        return True

    def run(self):
        cmd, time_limit = '', 1
        input_file, log_file,  = open(self.input_path), open(self.log_path, 'w')
        user_output_file, output_file = open(self.user_output_path, 'w+'), open(self.output_path)
        run_status = ('Accepted', True)

        if self.language == 'cpp' or self.language == 'cpp14' or self.language == 'c':
            cmd += ".\\a.exe"
        elif self.language == 'python':
            cmd += "python " + self.source_path
            time_limit = 5
        elif self.language == 'python3':
            cmd += "python3 " + self.source_path
            time_limit = 5

        try:
            subprocess.check_call(cmd, shell=True,
                                  stdout=user_output_file, stdin=input_file,
                                  stderr=log_file, timeout=time_limit, cwd=self.prob_wd)
        except subprocess.CalledProcessError:
            run_status = ("Runtime Error", False)
        except subprocess.TimeoutExpired:
            run_status = ("Time Limit Exceeded", False)

        if os.getcwd() == self.prob_wd:
            os.chdir(BASE_DIR)
        user_output_file.seek(0, 0)
        if not (output_file.read() == user_output_file.read()):
            run_status = ("Wrong Answer", False)

        log_file.close()
        user_output_file.close()
        output_file.close()
        input_file.close()
        os.remove(self.user_output_path)
        os.remove(self.log_path)
        if self.language in ('c', 'cpp', 'cpp14'):
            os.remove(os.path.join(self.prob_wd, 'a.exe'))

        return run_status


def eval_submission(problem_code, src_file_name, language):
    src_file_path = os.path.join(BASE_DIR, os.path.join(submissions_dir, src_file_name))
    input_file_path = os.path.join(BASE_DIR, os.path.join(os.path.join(test_data_dir, problem_code), 'input.txt'))
    output_file_path = os.path.join(BASE_DIR, os.path.join(os.path.join(test_data_dir, problem_code), 'output.txt'))
    log_file_path = os.path.join(BASE_DIR, os.path.join(os.path.join(test_data_dir, problem_code), 'log.txt'))
    user_output_file_path = os.path.join(BASE_DIR,
                                         os.path.join(os.path.join(test_data_dir, problem_code), 'user_output.txt'))

    program = Program(src_path=src_file_path, input_file=input_file_path,
                      output_file=output_file_path, log_file=log_file_path,
                      user_output=user_output_file_path, lang=language,
                      prob_code=problem_code)

    if language in ('c', 'cpp', 'cpp14'):
        if not program.compile():
            return 'Compile Time Error', False
    return program.run()
