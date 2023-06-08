FlexFarmer
========================================================================

Advanced syncless Chia farmer created to work with Flexpool.io.

Requirements
------------------------------------------------------------------------

- Initialized Plot NFT (Made via GUI or CLI)
- Plots bound to that Plot NFT
- NFT pooled to Flexpool (please see get started guide on our website for instructions)
- 100MB of RAM

Usage
------------------------------------------------------------------------

To start FlexFarmer on Linux, do:
    ./flexfarmer -c config.yml

Or with windows:
    flexfarmer.exe -c config.yml

This assumes that you have made the configuration file and saved it in the same folder as `config.yml`

Configuration
------------------------------------------------------------------------

You can find the config template in `config_template.yml`.

Here's a quick example of how the .yml config file will look like:

-----
plot_directories: ["/plotdir1", "/plotdir2"] # Directories (folder paths) where your plots are located.
farmer_secret_key: "0xf61398a76cdbd6ee5d0f31d757ca96c549876b287c0b19becd26e9e2990eae3e" # The secret key extracted from your mnemonic phrase. Please use `extract_farmer_key.py` Python script to extract the Farmer secret key.
launcher_id: "0x2be1162ad1148809bd01c81cea6eba4f9531fd7d330ab8df34404b5a33facd60" # Your launcher ID found in `chia plotnft show`, or in the GUI Pool Overview.
worker_name: myworker  # Arbitrary worker name. This will show on your Flexpool website dashboard. Feel free to choose any name under 10 characters.
region: us # Select the closest region here. Applicable values are `us`, `de`, `sg` (please enter your region without `` quotes).
payout_address: xch1fh6f088cxcvqscy4xtxfq7762vhsh9mjcql6m3svfhmlxsc3jd4sd37xdl  # The payout address to use. Both pool and farmer rewards will be pointed to it. It's reccomended not to use an exchange address.
-----

FAQ
========================================================================

- How to extract farmer secret key from mnemonic?
  
  Use `extract_farmer_key.py` Python script.

- Does FlexFarmer program charge any fees?

  No.

- Can my XCH be stolen with the secret key?

  Short answer: No. Long answer, only 0.25 XCH farmer reward can be stolen,
  and only if the hacker is having access to both your farmer secret key,
  and the plot local secret key, which is located in the plot header.
  All this also assumes that the hacker will be able to intercept the block
  before it was sent to other nodes.

- In case if a certain Flexpool.io region is having issues, will my farm failover to another region?

  Yes. FlexFarmer has a built-in automatic failover system that will try to
  connect to neighbor regions in case if something is wrong with the
  primary location.