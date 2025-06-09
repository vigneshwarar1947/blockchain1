pragma solidity ^0.8.21;
//SPDX-License-Identifier: MIT

contract CertificateStore {
    // Mapping to track if a certificate hash exists
    mapping(bytes32 => bool) public certificateExists;

    // Event emitted when a certificate hash is stored
    event CertificateStored(bytes32 certificateHash);

    // Store a certificate hash on the blockchain.
    function storeCertificate(bytes32 _certificateHash) public {
        require(!certificateExists[_certificateHash], "Certificate already stored.");
        certificateExists[_certificateHash] = true;
        emit CertificateStored(_certificateHash);
    }

    // Verify whether a certificate hash exists.
    function verifyCertificate(bytes32 _certificateHash) public view returns (bool) {
        return certificateExists[_certificateHash];
    }
}
