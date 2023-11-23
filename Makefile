run_cli_pares: pairs.py
	python3 cliente.py $(arg)

run_serv_pares_1: pairs.py
	python3 servidor.py $(arg)

run_serv_pares_2: pairs.py
	python3 servidor.py $(arg) flag

run_serv_central: pairs.py
	python3 servidor_cent.py $(arg)

run_cli_central: pairs.py
	python3 cliente_cent.py $(arg)

pairs.py: pares.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pares.proto

clean:
	rm -f *_pb2.py *_pb2_grpc.py