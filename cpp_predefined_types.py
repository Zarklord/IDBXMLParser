def apply_predefined_types(cpp_global):
    cpp_global.add_type("void", 0, "")

    cpp_global.add_type("int8_t", 1, "/stdint.h")
    cpp_global.add_type("uint8_t", 1, "/stdint.h")

    cpp_global.add_type("int16_t", 2, "/stdint.h")
    cpp_global.add_type("uint16_t", 2, "/stdint.h")

    cpp_global.add_type("int32_t", 4, "/stdint.h")
    cpp_global.add_type("uint32_t", 4, "/stdint.h")

    cpp_global.add_type("int64_t", 8, "/stdint.h")
    cpp_global.add_type("uint64_t", 8, "/stdint.h")