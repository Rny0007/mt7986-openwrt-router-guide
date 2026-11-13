# First Boot & Initial Configuration

Following a successful OpenWrt installation, perform these foundational configuration steps to establish administrative security, key-based authentication, and system time synchronization.

---

## 1. Initial Access to LuCI Web Interface

1. Connect your computer to any LAN port (`lan1`–`lan4`) using an Ethernet cable.
2. Ensure your computer obtains an IP address via DHCP (typically `192.168.1.xxx`).
3. Open a web browser and navigate to:
   `http://192.168.1.1`
4. On fresh installation, the default username is `root` with **no password**.
5. Click **Login**.

---

## 2. Set Administrator Password

Immediately establish a strong administrator password:

1. In LuCI, navigate to **System** → **Administration** → **Router Password**.
2. Enter a strong, unique password.
3. Click **Save & Apply**.

> [!IMPORTANT]
> Once a password is set, LuCI requires authentication, and Dropbear SSH enables password authentication for the `root` account.

---

## 3. SSH Key-Based Authentication

Passwordless, cryptographic key authentication is significantly more secure than password authentication.

### Step 3.1: Generate an Ed25519 Key Pair (Host Machine)
On your host terminal (PowerShell / Linux Terminal):

```sh
# Generate a dedicated Ed25519 key pair
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_openwrt -C "openwrt-admin"
```

### Step 3.2: Install Public Key in OpenWrt

#### Option A: Via LuCI Web Interface
1. Navigate to **System** → **Administration** → **SSH-Keys**.
2. Paste the contents of your public key (`id_ed25519_openwrt.pub`).
3. Click **Save & Apply**.

#### Option B: Via SSH Command Line
```sh
# Append public key to authorized_keys on the router
cat ~/.ssh/id_ed25519_openwrt.pub | ssh root@192.168.1.1 "cat >> /etc/dropbear/authorized_keys"
```

### Step 3.3: Verify Key Authentication
Test logging in using your private key:

```sh
ssh -i ~/.ssh/id_ed25519_openwrt root@192.168.1.1
```

Once verified, you may optionally disable password authentication under **System** → **Administration** → **SSH Access** (check `Allow SSH password authentication` to `off`).

---

## 4. NTP Time Synchronization

Accurate system time is essential for DNSSEC validation, SSL/TLS handshakes, and log timestamps.

1. Navigate to **System** → **System** → **Time Synchronization**.
2. Verify NTP client is **Enabled**.
3. Default pool servers (`0.openwrt.pool.ntp.org` to `3.openwrt.pool.ntp.org`) are pre-configured.
4. Set your local **Timezone** (e.g. `Asia/Kolkata` or `UTC`).
5. Click **Save & Apply**.

---

## 5. Software Package Index Update

Verify internet access and update the package repository index:

```sh
# [Router SSH]
opkg update
```

*(Note: OpenWrt 25.12 includes `apk` in select builds; if your image utilizes `apk`, use `apk update`)*.
