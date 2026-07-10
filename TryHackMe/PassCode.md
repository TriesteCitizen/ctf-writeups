<h1 align="center">Challenge 070 - PassCode </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/59d8689b-3a8a-4908-8b2a-f306d467a1f7" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

We may have found a way to break into the DarkInject blockchain, exploiting a vulnerability in their system. This might be our only chance to stop them - for good.

```
root@attacker:~# RPC_URL=http://10.112.134.90:8545
root@attacker:~# API_URL=http://10.112.134.90
root@attacker:~# PRIVATE_KEY=$(curl -s ${API_URL}/challenge | jq -r ".player_wallet.private_key")
root@attacker:~# CONTRACT_ADDRESS=$(curl -s ${API_URL}/challenge | jq -r ".contract_address")
root@attacker:~# PLAYER_ADDRESS=$(curl -s ${API_URL}/challenge | jq -r ".player_wallet.address")
root@attacker:~# is_solved=`cast call $CONTRACT_ADDRESS "isSolved()(bool)" --rpc-url ${RPC_URL}`
root@attacker:~# echo "Check if is solved: $is_solved"
Check if is solved: false
```

The output indicates that the challenge has not been solved yet (isSolved return false). You need to find out what is required to solve the challenge. This typically involves retrieving a passcode or key from the smart contract storage, and then submitting it to the contract using a transaction. First, try checking the contract storage to see if you can retrieve the necessary passcode or key. You can do this with the following command:
`cast storage $CONTRACT_ADDRESS 0 --rpc`

The lab machine IP shows the following:

<img width="1087" height="720" alt="image" src="https://github.com/user-attachments/assets/db360efb-7a99-4765-8f8b-7af81c135a85" />

There also is source code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Challenge {
    string private secret = "THM{}";
    bool private unlock_flag = false;
    uint256 private code;
    string private hint_text;
    
    constructor(string memory flag, string memory challenge_hint, uint256 challenge_code) {
        secret = flag;
        code = challenge_code;
        hint_text = challenge_hint;
    }
    
    function hint() external view returns (string memory) {
        return hint_text;
    }
    
    function unlock(uint256 input) external returns (bool) {
        if (input == code) {
            unlock_flag = true;
            return true;
        }
        return false;
    }
    
    function isSolved() external view returns (bool) {
        return unlock_flag;
    }
    
    function getFlag() external view returns (string memory) {
        require(unlock_flag, "Challenge not solved yet");
        return secret;
    }
}
```
This Solidity contract defines a simple challenge system. It has the following key components:

**1. State Variables**:
- `secret`: A private string that holds the flag("THM{[redacted - find it yourself!]}") which can only be retrieved if the challenge is solved.
- `unlock_flag`: A boolean that indicates whether the challenge has been solved.
- `code`: A uint256 that stores the passcode required to unlock the challenge.
- `hint_text`: A private string that provides hints related to the challenge.

**2. Constructor**: Initializes the contract with a flag, hint text, and challenge code when deployed.

**3. Functions**:
- `hint()`: Allows users to retrieve the hint text.
- `unlock(uint256 input)`: Accepts a numeric input and checks if it matches the `code`. If it does, it sets `unlock_flag` to true and returns true; otherwise, it returns false.
- `isSolved()`: Returns the value of `unlock_flag`, indicating if the challenge has been solved.
- `getFlag()`: Returns the `secret` if the challenge is solved; otherwise, it throws an error requiring that the challenge is solved

In summary, this contract requires users to input the correct `code` to unlock and retrieve the `secret`. The `hint` function provides additional context to aid in solving the challenge.

Blockchain is a decentralized digital ledger technology that records transactions across many computers securely and transparently. Each transaction is grouped into blocks, which are linked together in chronological order, forming a chain. In the context of the challenge, we are working with a blockchain smart contract that requires us to interact with it to solve a passcode challenge. To begin we should first ensure that we have the correct API and RPC endpoints set up to communicate with the blockchain. We can start by querying the challenge API to gather the necessary information like our wallet's private key and the contract address. We can use the following command to check the initial challenge context:

`curl -s http://10.112.134.90/challenge

```
root@ip-10-112-77-245:~# curl -s http://10.112.134.90/challenge
{"name":"blockchain","description":"Goal: have the isSolved() function return true","status":"DEPLOYED","blockTime":0,"rpc_url":"http://geth:8545","player_wallet":{"address":"0x370dD98e3a89845D5A0217605A7D33389095B186","private_key":"0x5469381de039964248a65d8092352e0a7aae2108dcc6934d579648f889943433","balance":"1.0 ETH"},"contract_address":"0xab9A67BDA6C35E84B64F48A12c668978A450c7B0"}`
```

We export the private key, contract address, and player address to environment variables using the following commands:

```
export PRIVATE_KEY="0x5469381de039964248a65d8092352e0a7aae2108dcc6934d579648f889943433"
export CONTRACT_ADDRESS="0xab9A67BDA6C35E84B64F48A12c668978A450c7B0"
export PLAYER_ADDRESS="0x370dD98e3a89845D5A0217605A7D33389095B186"
```


When checking the other port a file gets downloaded: `/root/Downloads/ZxK8s8Jd`

