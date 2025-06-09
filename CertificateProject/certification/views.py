# Create your views here.
# certification/views.py
import hashlib
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CertificateForm, VerifyCertificateForm
from .models import Certificate
from web3 import Web3

# Connect to your blockchain node (e.g., Ganache)
blockchain_url = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(blockchain_url))

# Validate Web3 Connection
if not w3.is_connected():
    raise ConnectionError("Web3 provider is not connected. Check your blockchain node.")

# Load contract ABI and set contract address (update these as necessary)
try:
    with open('certification/contract_abi.json', 'r') as abi_file:
        abi_data = json.load(abi_file)  # Load the ABI JSON correctly
        contract_abi = abi_data.get("abi", [])  # Extract the ABI list
except Exception as e:
    raise ValueError(f"Error loading ABI file: {e}")

# Validate ABI format
if not isinstance(contract_abi, list):
    raise TypeError(f"Contract ABI must be a list, found {type(contract_abi)}")

# Convert contract address to checksum format
contract_address = Web3.to_checksum_address("0x6becd4edab083126df7529001f96c47afbffab87")

# Debugging print to verify checksum conversion
print(f"Checksum Address: {contract_address}")  

# Initialize the contract correctly
certificate_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Set the default account (ensure this account has sufficient funds on your local blockchain)
if w3.eth.accounts:
    default_account = w3.eth.accounts[0]
    w3.eth.default_account = default_account
else:
    raise ValueError("No accounts found on Web3 provider. Make sure your node is running.")

def compute_file_hash(file):
    """Compute SHA-256 hash of the uploaded file."""
    sha256 = hashlib.sha256()
    for chunk in file.chunks():
        sha256.update(chunk)
    return "0x" + sha256.hexdigest()

def submit_certificate(request):
    """View for institute users to submit a certificate."""
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            student_name = form.cleaned_data['student_name']
            certificate_file = form.cleaned_data['certificate_file']
            file_hash = compute_file_hash(certificate_file)

            try:
                print(f"Submitting certificate with hash: {file_hash}")  

                tx_hash = certificate_contract.functions.storeCertificate(
                    bytes.fromhex(file_hash[2:])  # Convert hex string to bytes
                ).transact({'from': default_account})  # Specify sender explicitly

                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            except Exception as e:
                messages.error(request, f"Blockchain transaction failed: {e}")
                return render(request, 'certification/certificate_form.html', {'form': form})

            Certificate.objects.create(
                student_name=student_name,
                certificate_file=certificate_file,
                certificate_hash=file_hash,
                blockchain_tx=tx_hash.hex()
            )
            messages.success(request, "Certificate stored successfully!")
            return render(request, 'certification/certificate_form.html', {'form': CertificateForm()})
          

    else:
        form = CertificateForm()

    return render(request, 'certification/certificate_form.html', {'form': form})
def verify_certificate(request):
    if request.method == 'POST':
        form = VerifyCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate_file = form.cleaned_data['certificate_file']
            file_hash = compute_file_hash(certificate_file)

            try:
                cert_hash_bytes = bytes.fromhex(file_hash[2:])
                print("Verifying hash (bytes32):", cert_hash_bytes)
                print("Length:", len(cert_hash_bytes))  # Should be 32

                exists = certificate_contract.functions.verifyCertificate(cert_hash_bytes).call()
                print("Exists on blockchain:", exists)

            except Exception as e:
                print("Blockchain call error:", e)
                messages.error(request, f"Blockchain query failed: {e}")
                return render(request, 'certification/verify_certificate.html', {'form': form})

            if exists:
                messages.success(request, "Certificate is valid !")
                return render(request, 'certification/verify_certificate.html', {'form': VerifyCertificateForm()})
            else:
                messages.error(request, "Invalid Certificate ")
                return render(request, 'certification/verify_certificate.html', {'form': VerifyCertificateForm()})
            
            return redirect('certificate_verified')
    else:
        form = VerifyCertificateForm()

    return render(request, 'certification/verify_certificate.html', {'form': form})




def certificate_success(request):
    """Display a success message after certificate submission."""
    return render(request, 'certification/certificate_success.html')

def certificate_verified(request):
    """Display the result after certificate verification."""
    return render(request, 'certification/certificate_verified.html')
