import heapq
import os
import pickle
from collections import Counter, defaultdict
from typing import Dict, Tuple, Optional


class HuffmanNode:
    """哈夫曼树节点类"""

    def __init__(self, char: Optional[str], freq: int):
        self.char = char  # 字符（None表示内部节点）
        self.freq = freq  # 频率
        self.left = None
        self.right = None

    def __lt__(self, other):
        # 使节点可以比较，用于优先队列
        return self.freq < other.freq


class HuffmanCoding:
    """哈夫曼编码与文件压缩类"""

    def __init__(self):
        self.codes = {}  # 字符到哈夫曼编码的映射
        self.reverse_mapping = {}  # 哈夫曼编码到字符的反向映射

    def build_frequency_dict(self, text: str) -> Dict[str, int]:
        """统计字符频率"""
        return dict(Counter(text))

    def build_huffman_tree(self, frequency: Dict[str, int]) -> Optional[HuffmanNode]:
        """构建哈夫曼树"""
        if not frequency:
            return None

        # 创建优先队列（最小堆）
        heap = []
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)

        # 构建哈夫曼树
        while len(heap) > 1:
            # 取出两个最小频率的节点
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            # 创建新节点作为它们的父节点
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(heap, merged)

        return heap[0] if heap else None

    def generate_codes_helper(self, root: HuffmanNode, current_code: str):
        """递归生成哈夫曼编码"""
        if root is None:
            return

        # 如果是叶子节点，保存编码
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        # 递归处理左右子树
        self.generate_codes_helper(root.left, current_code + "0")
        self.generate_codes_helper(root.right, current_code + "1")

    def generate_codes(self, root: HuffmanNode):
        """生成哈夫曼编码表"""
        if root is None:
            return
        self.codes.clear()
        self.reverse_mapping.clear()
        self.generate_codes_helper(root, "")

    def get_encoded_text(self, text: str) -> str:
        """将文本编码为哈夫曼编码"""
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text: str) -> str:
        """填充编码文本使其长度为8的倍数"""
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        # 将填充信息以8位二进制形式添加到开头
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text: str) -> bytearray:
        """将二进制字符串转换为字节数组"""
        if len(padded_encoded_text) % 8 != 0:
            print("编码文本长度不是8的倍数")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte_segment = padded_encoded_text[i:i + 8]
            b.append(int(byte_segment, 2))
        return b

    def compress(self, input_path: str, output_path: str):
        """压缩文件"""
        print("正在压缩文件...")

        # 1. 读取文件并统计字符频率
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        if not text:
            print("文件为空，无需压缩")
            return

        # 2. 构建哈夫曼树
        frequency = self.build_frequency_dict(text)
        huffman_tree = self.build_huffman_tree(frequency)

        # 3. 生成哈夫曼编码
        self.generate_codes(huffman_tree)

        # 4. 编码文本
        encoded_text = self.get_encoded_text(text)

        # 5. 填充并转换为字节
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)

        # 6. 保存压缩文件（包含编码表）
        with open(output_path, 'wb') as output:
            # 保存频率字典
            pickle.dump(frequency, output)
            # 保存原始文本长度（用于解码时去除填充）
            pickle.dump(len(text), output)
            # 保存压缩数据
            output.write(bytes(byte_array))

        # 7. 计算压缩率
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        compression_ratio = (1 - output_size / input_size) * 100

        print(f"压缩完成!")
        print(f"原始文件大小: {input_size} 字节")
        print(f"压缩后大小: {output_size} 字节")
        print(f"压缩率: {compression_ratio:.2f}%")

        return compression_ratio

    def remove_padding(self, padded_encoded_text: str) -> str:
        """去除填充位"""
        # 获取填充信息
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        # 去除填充信息
        padded_encoded_text = padded_encoded_text[8:]

        # 去除实际填充位
        if extra_padding > 0:
            encoded_text = padded_encoded_text[:-extra_padding]
        else:
            encoded_text = padded_encoded_text

        return encoded_text

    def decode_text(self, encoded_text: str) -> str:
        """解码文本"""
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""

        return decoded_text

    def decompress(self, input_path: str, output_path: str):
        """解压缩文件"""
        print("正在解压缩文件...")

        # 1. 读取压缩文件
        with open(input_path, 'rb') as file:
            # 读取频率字典
            frequency = pickle.load(file)
            # 读取原始文本长度
            original_length = pickle.load(file)
            # 读取压缩数据
            bit_string = ""

            byte = file.read(1)
            while byte:
                # 将字节转换为8位二进制字符串
                byte_val = ord(byte)
                bits = bin(byte_val)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

        # 2. 重建哈夫曼树
        huffman_tree = self.build_huffman_tree(frequency)

        # 3. 生成编码表
        self.generate_codes(huffman_tree)

        # 4. 去除填充并解码
        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)

        # 5. 写入解压后的文件
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)

        print(f"解压完成! 文件已保存到 {output_path}")

        return decompressed_text


def test_huffman_coding():
    """测试哈夫曼编码与压缩"""

    # 创建测试文本
    test_text = """哈夫曼编码是一种用于无损数据压缩的熵编码算法。
该算法使用变长编码表对源符号进行编码，其中变长编码表是通过评估源符号出现概率的方法得到的。
出现概率高的符号使用较短的编码，反之出现概率低的则使用较长的编码。
这使得编码之后的字符串的平均长度、期望值降低，从而达到无损压缩数据的目的。"""

    # 保存测试文件
    input_file = "test_input.txt"
    compressed_file = "test_compressed.bin"
    decompressed_file = "test_decompressed.txt"

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_text)

    # 创建哈夫曼编码器
    huffman = HuffmanCoding()

    # 1. 测试字符频率统计
    print("=== 字符频率统计 ===")
    frequency = huffman.build_frequency_dict(test_text)
    print(f"总字符数: {len(test_text)}")
    print(f"不同字符数: {len(frequency)}")
    print("前10个最常见字符:")
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10]
    for char, freq in sorted_freq:
        print(f"  '{char}': {freq}")

    # 2. 构建哈夫曼树
    print("\n=== 构建哈夫曼树 ===")
    huffman_tree = huffman.build_huffman_tree(frequency)
    print("哈夫曼树构建完成!")

    # 3. 生成哈夫曼编码
    print("\n=== 哈夫曼编码表 ===")
    huffman.generate_codes(huffman_tree)
    print(f"生成的编码数量: {len(huffman.codes)}")
    print("部分编码示例:")
    for i, (char, code) in enumerate(list(huffman.codes.items())[:10]):
        print(f"  '{char}': {code}")

    # 4. 压缩文件
    print("\n=== 文件压缩 ===")
    compression_ratio = huffman.compress(input_file, compressed_file)

    # 5. 解压缩文件
    print("\n=== 文件解压缩 ===")
    decompressed_text = huffman.decompress(compressed_file, decompressed_file)

    # 6. 验证解压缩结果
    print("\n=== 验证结果 ===")
    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    if original_text == decompressed_text:
        print("✓ 解压缩成功，内容完全一致!")
    else:
        print("✗ 解压缩失败，内容不一致!")

    # 7. 清理测试文件
    os.remove(input_file)
    os.remove(compressed_file)
    os.remove(decompressed_file)

    return compression_ratio


def compress_file():
    """压缩用户指定的文件"""
    input_file = input("请输入要压缩的文件路径: ").strip()

    if not os.path.exists(input_file):
        print("文件不存在!")
        return

    output_file = input("请输入压缩后文件路径（默认: compressed.bin）: ").strip()
    if not output_file:
        output_file = "compressed.bin"

    huffman = HuffmanCoding()
    huffman.compress(input_file, output_file)


def decompress_file():
    """解压缩用户指定的文件"""
    input_file = input("请输入要解压缩的文件路径: ").strip()

    if not os.path.exists(input_file):
        print("文件不存在!")
        return

    output_file = input("请输入解压后文件路径（默认: decompressed.txt）: ").strip()
    if not output_file:
        output_file = "decompressed.txt"

    huffman = HuffmanCoding()
    huffman.decompress(input_file, output_file)


def main():
    """主函数"""
    print("=" * 50)
    print("哈夫曼编码与文件压缩系统")
    print("=" * 50)

    while True:
        print("\n请选择操作:")
        print("1. 运行测试示例")
        print("2. 压缩文件")
        print("3. 解压缩文件")
        print("4. 退出")

        choice = input("请输入选项 (1-4): ").strip()

        if choice == "1":
            print("\n运行测试示例...")
            test_huffman_coding()
        elif choice == "2":
            compress_file()
        elif choice == "3":
            decompress_file()
        elif choice == "4":
            print("感谢使用，再见!")
            break
        else:
            print("无效选项，请重新输入!")


if __name__ == "__main__":
    main()