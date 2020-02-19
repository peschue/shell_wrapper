# shell_wrapper

Protobuf-based service for generic Shell Applications, indented for usage in Acumos in the AI4EU Project.

# How to run

* `$ ./run_test.sh`

  This will start a server that can run the binary specified in https://github.com/peschue/shell_wrapper/blob/master/shell_wrapper_daemon.py
  
  Then it will run the test client that sends a request and prints the result.
  
  At the moment this uses the `clingo` ASP Solver to illustrate the functionality. Clingo can be obtained from https://github.com/potassco/clingo/ or via `conda`
