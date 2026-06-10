cmake_minimum_required(VERSION 3.10.0)
project(AlgoritmosInteligenciaArtificial-imperative VERSION 0.1.0 LANGUAGES C CXX)

# gRPC requiere C++14 o superior
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Buscar los paquetes oficiales de MSYS2
find_package(protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

# Es fundamental incluir los archivos .cc generados por protoc
add_executable(AlgoritmosInteligenciaArtificial-imperative 
    main.cpp
    ../../proto/ml_contract.pb.cc
    ../../proto/ml_contract.grpc.pb.cc
)

# Enlace de las librerías utilizando los nombres de destino correctos de MSYS2
target_link_libraries(AlgoritmosInteligenciaArtificial-imperative
    PRIVATE
    gRPC::grpc++
    protobuf::libprotobuf
)

target_include_directories(
    AlgoritmosInteligenciaArtificial-imperative
    PRIVATE
    ../../proto
)