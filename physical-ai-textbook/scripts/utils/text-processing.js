/**
 * Utility functions for text processing
 */

/**
 * Chunk text into smaller pieces with overlap
 * @param {string} text - The text to chunk
 * @param {number} chunkSize - The size of each chunk in characters
 * @param {number} overlap - The overlap between chunks in characters
 * @returns {Array} Array of chunk objects
 */
function chunkText(text, chunkSize = 1000, overlap = 100) {
    const chunks = [];
    let start = 0;
    const textLength = text.length;

    while (start < textLength) {
        let end = start + chunkSize;

        // If we're near the end, take the remaining text
        if (end > textLength) {
            end = textLength;
        }

        const chunk = text.substring(start, end);
        chunks.push({
            text: chunk,
            id: `chunk_${start}_${end}`,
        });

        // Move start position by chunkSize - overlap
        start = end - overlap;
    }

    return chunks;
}

module.exports = {
    chunkText
};