"""A collection of stuff related to https://stalburg.net/Body_message#Pegs."""
from infra.encodings.binary import binary_decode
from textures.metro_control_panel_001_pegboard import (metro_control_panel_001_pegboard, _invert_bool_list,
                                                       _bools_to_binary_str, _bools_to_nor_mask, _pegs_to_bool_list)

mp = metro_control_panel_001_pegboard


if __name__ == "__main__":
    def transform_pegs(a: str, mask: str, b: str) -> str:
        a_ = _pegs_to_bool_list(a)
        mask_ = _bools_to_nor_mask(mask)
        b_ = _pegs_to_bool_list(b)
        transformed = [op(first, second) for first, op, second in zip(a_, mask_, b_)]
        bytes_str = binary_decode(_bools_to_binary_str(transformed))
        return " ".join(char if 126 > ord(char) > 33 else str(ord(char)) for char in bytes_str)

    def transform_pegs_all_inverted(a: str, mask: str, b: str) -> str:
        a_ = _invert_bool_list(_pegs_to_bool_list(a))
        mask_ = _bools_to_nor_mask(mask)
        b_ = _invert_bool_list(_pegs_to_bool_list(b))
        transformed = [op(first, second) for first, op, second in zip(a_, mask_, b_)]
        bytes_str = binary_decode(_bools_to_binary_str(transformed))
        return " ".join(char if 126 > ord(char) > 33 else str(ord(char)) for char in bytes_str)

    def transform_pegs_top_inverted(a: str, mask: str, b: str) -> str:
        a_ = _invert_bool_list(_pegs_to_bool_list(a))
        mask_ = _bools_to_nor_mask(mask)
        b_ = (_pegs_to_bool_list(b))
        transformed = [op(first, second) for first, op, second in zip(a_, mask_, b_)]
        bytes_str = binary_decode(_bools_to_binary_str(transformed))
        return " ".join(char if 126 > ord(char) > 33 else str(ord(char)) for char in bytes_str)

    def transform_pegs_bottom_inverted(a: str, mask: str, b: str) -> str:
        a_ = (_pegs_to_bool_list(a))
        mask_ = _bools_to_nor_mask(mask)
        b_ = _invert_bool_list(_pegs_to_bool_list(b))
        transformed = [op(first, second) for first, op, second in zip(a_, mask_, b_)]
        bytes_str = binary_decode(_bools_to_binary_str(transformed))
        return " ".join(char if 126 > ord(char) > 33 else str(ord(char)) for char in bytes_str)

    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from top markers
        print(transform_pegs(panel[0],
                             panel[0],
                             panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from top markers
        print(transform_pegs(panel[1],
                             panel[0],
                             panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from bottom markers
        print(transform_pegs(panel[1],
                             panel[1],
                             panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from bottom markers
        print(transform_pegs(panel[0],
                             panel[1],
                             panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from top markers pegs inverted
        print(transform_pegs_all_inverted(panel[0],
                                          panel[0],
                                          panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from top markers inverted
        print(transform_pegs_all_inverted(panel[1],
                                          panel[0],
                                          panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from bottom markers inverted
        print(transform_pegs_all_inverted(panel[1],
                                          panel[1],
                                          panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from bottom markers inverted
        print(transform_pegs_all_inverted(panel[0],
                                          panel[1],
                                          panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from top markers pegs inverted
        print(transform_pegs_top_inverted(panel[0],
                                          panel[0],
                                          panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from top markers inverted
        print(transform_pegs_top_inverted(panel[1],
                                          panel[0],
                                          panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from bottom markers inverted
        print(transform_pegs_top_inverted(panel[1],
                                          panel[1],
                                          panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from bottom markers inverted
        print(transform_pegs_top_inverted(panel[0],
                                          panel[1],
                                          panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from top markers pegs inverted
        print(transform_pegs_bottom_inverted(panel[0],
                                             panel[0],
                                             panel[1]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from top markers inverted
        print(transform_pegs_bottom_inverted(panel[1],
                                             panel[0],
                                             panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # bottom nor top from bottom markers inverted
        print(transform_pegs_bottom_inverted(panel[1],
                                             panel[1],
                                             panel[0]))
    print()
    for panel in metro_control_panel_001_pegboard:
        # top nor bottom from bottom markers inverted
        print(transform_pegs_bottom_inverted(panel[0],
                                             panel[1],
                                             panel[1]))
