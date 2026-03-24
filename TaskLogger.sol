// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// TaskLogger.sol — TaskChain AI Smart Contract
// Deploy on Shardeum Sphinx Testnet (or any EVM chain)
// Stores AI analysis results permanently on-chain

contract TaskLogger {

    // ─── STRUCTS ──────────────────────────────────────────────────
    struct TaskLog {
        bytes32 messageHash;   // keccak256 of original message
        string  priority;      // "High" | "Medium" | "Low"
        string  category;      // "Sales" | "Support" | "General"
        uint256 timestamp;
        address logger;        // wallet that logged this entry
    }

    // ─── STATE ────────────────────────────────────────────────────
    TaskLog[] public logs;
    address public owner;

    // ─── EVENTS ───────────────────────────────────────────────────
    event TaskLogged(
        uint256 indexed logId,
        bytes32 indexed messageHash,
        string  priority,
        string  category,
        uint256 timestamp,
        address logger
    );

    // ─── CONSTRUCTOR ──────────────────────────────────────────────
    constructor() {
        owner = msg.sender;
    }

    // ─── FUNCTIONS ────────────────────────────────────────────────

    /**
     * @notice Log an AI-analyzed task to the blockchain
     * @param _messageHash  keccak256 hash of the original customer message
     * @param _priority     AI-determined priority level
     * @param _category     AI-determined category
     */
    function logTask(
        bytes32 _messageHash,
        string calldata _priority,
        string calldata _category
    ) external returns (uint256 logId) {
        logId = logs.length;

        logs.push(TaskLog({
            messageHash: _messageHash,
            priority:    _priority,
            category:    _category,
            timestamp:   block.timestamp,
            logger:      msg.sender
        }));

        emit TaskLogged(logId, _messageHash, _priority, _category, block.timestamp, msg.sender);
    }

    /**
     * @notice Get a single log entry by index
     */
    function getLog(uint256 _id) external view returns (TaskLog memory) {
        require(_id < logs.length, "Log does not exist");
        return logs[_id];
    }

    /**
     * @notice Get total number of logs
     */
    function totalLogs() external view returns (uint256) {
        return logs.length;
    }

    /**
     * @notice Get the last N logs (for dashboard display)
     */
    function getRecentLogs(uint256 _count) external view returns (TaskLog[] memory) {
        uint256 total = logs.length;
        uint256 count = _count > total ? total : _count;
        TaskLog[] memory recent = new TaskLog[](count);
        for (uint256 i = 0; i < count; i++) {
            recent[i] = logs[total - count + i];
        }
        return recent;
    }
}

/*
 ═══════════════════════════════════════════════════
  DEPLOYMENT INSTRUCTIONS (Shardeum Sphinx Testnet)
 ═══════════════════════════════════════════════════

  1. Go to remix.ethereum.org
  2. Create a new file: TaskLogger.sol, paste this code
  3. Compile with Solidity ^0.8.19
  4. In "Deploy & Run":
       - Environment: "Injected Provider - MetaMask"
       - Network: Shardeum Sphinx 1.X Testnet
         RPC: https://sphinx.shardeum.org/
         Chain ID: 8082
  5. Click Deploy → confirm in MetaMask
  6. Copy the contract address

  TO CALL FROM PYTHON (web3.py):

    from web3 import Web3
    import json, hashlib

    w3 = Web3(Web3.HTTPProvider("https://sphinx.shardeum.org/"))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

    msg_hash = w3.keccak(text=customer_message)
    tx = contract.functions.logTask(msg_hash, priority, category).build_transaction({
        'from': YOUR_WALLET, 'nonce': w3.eth.get_transaction_count(YOUR_WALLET)
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("TX:", tx_hash.hex())

 ═══════════════════════════════════════════════════
*/
