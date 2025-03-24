import csv
from web3 import Web3

INFURA_URL = "https://mainnet.infura.io/v3/2f5c733c71b244a1ab4832b54e2d4b51"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if w3.is_connected():
    print("Connected to Infura!")
else:
    print("Failed to connect.")

start_block = 17000000  # 起始区块号
num_blocks = 5000  # 采样 5000 个区块
sample_interval = 50  # 每 50 个区块采样一次
tx_per_block = 10  # 每个区块取前 10 笔交易
csv_filename = "/Users/yishu/Desktop/sampled_transactions.csv"
# 创建 CSV 文件
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["tx_hash", "from", "to", "value", "gasPrice", "gasUsed", "blockNumber"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    total_tx_count = 0  # 统计总交易数

    for block_number in range(start_block, start_block + num_blocks, sample_interval):
        try:
            block = w3.eth.get_block(block_number, full_transactions=True)
            transactions = block.transactions[:tx_per_block]  # 取前 10 笔交易

            for tx in transactions:
                tx_data = {
                    "tx_hash": tx.hash.hex(),
                    "from": tx["from"],
                    "to": tx["to"],
                    "value": w3.from_wei(tx["value"], "ether"),
                    "gasPrice": w3.from_wei(tx["gasPrice"], "gwei"),
                    "gasUsed": tx["gas"],
                    "blockNumber": block_number
                }
                writer.writerow(tx_data)

            total_tx_count += len(transactions)
            print(f"Processed block {block_number}, total transactions saved: {total_tx_count}")

        except Exception as e:
            print(f"Error processing block {block_number}: {e}")

print(f"Total {total_tx_count} transactions saved to {csv_filename}")
