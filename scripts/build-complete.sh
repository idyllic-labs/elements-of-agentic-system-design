#!/bin/bash

# Build a single complete document from all element files
# Output: complete-elements.md

OUTPUT_FILE="complete-elements.md"
ELEMENTS_DIR="elements"

echo "Building complete elements document..."

# Start with the README
cat "README.md" > "$OUTPUT_FILE"
echo -e "\n---\n" >> "$OUTPUT_FILE"
echo "# Element Reference" >> "$OUTPUT_FILE"
echo -e "\n---\n" >> "$OUTPUT_FILE"

# Concatenate all element files in order
for i in {1..10}; do
    FILE=$(ls "$ELEMENTS_DIR"/${i}-*.md 2>/dev/null)
    if [ -f "$FILE" ]; then
        echo "Adding: $FILE"
        cat "$FILE" >> "$OUTPUT_FILE"
        echo -e "\n---\n" >> "$OUTPUT_FILE"
    else
        echo "Warning: Element $i not found"
    fi
done

# Count words and elements
WORD_COUNT=$(wc -w < "$OUTPUT_FILE")
echo ""
echo "Complete document built: $OUTPUT_FILE"
echo "Total words: $WORD_COUNT"
