ARC3 Reference Implementation
-----------------------------

This repository contains an implementation of a dapp that can be used to Mint [ARC3](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md) compliant NFTs

A [live demo](https://arc3.xyz) is available.


Status:
-------

Its hosted by [Cloudflare](https://pages.dev) but I cant get it to build there so I just committed my build directory

Intention is to build Components to validate and display any Asset type that is minted (Images, GIFS, Audio, Video, PDFs, ...) and possibly collections and fractional NFTs

A standalone npm package to parse and validate the metadata would be nice to have. 

Also it looks meh and needs a logo 

PRs very welcome

I have my _personal_ web3.storage token set in the config, this is not great practice but I'm trusting you not to spam me. Also know that I can unpin/delete these files from IPFS at any time, so you'll have to trust me as well.


Devs
-----

To hack on it, start by registering for an account with [web3.storage](https://web3.storage), they provide up to 1TB of IPFS storage.

```
git clone https://github.com/barnjamin/arc3.xyz.git
cd arc3.xyz
yarn install
```

In this repo we're using a cloudflare worker to add the bearer token to the headers before proxying the request to web3.storage. This helps keep the key secret but for testing purposes you can set your storage token in a local config file.

1. Set your key in the `storageToken` field in `src/config.json` and update whatever other fields there you'd like 
2. Uncomment the storage var in `src/lib/ipfs.ts` and comment the one pointing to the barnji worker


```
yarn start
```

Right now, this will open a browser window with a warning about security, you can proceed in chrome by clicking advanced and proceed.  The reason for this warning is that some cryptographic libraries require HTTPS to load and the certificate is not valid for this project yet.

I did try to create one with mkcert but browser still complained that CA was invalid.

The Wallet Session connection is provided by https://github.com/barnjamin/algorand-session-wallet  and supports AlgoSigner, MyAlgo, WalletConnect and an Insecure Wallet (don't use with MainNet accts)
