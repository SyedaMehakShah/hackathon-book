#!/usr/bin/env node

/**
 * Script to validate all textbook content
 * Usage: node scripts/validate-content.js
 */

const fs = require('fs').promises;
const path = require('path');

// Configuration
const DOCS_DIR = path.join(__dirname, '../docs');

// Validation rules
const validationRules = {
    // Minimum length for a content section
    minContentLength: 50,
    
    // Required frontmatter fields (for systems that use them)
    requiredFrontmatter: [],
    
    // Allowed file extensions
    allowedExtensions: ['.md'],
    
    // Required sections in each chapter
    requiredSections: ['Introduction', 'Summary'],
    
    // Pattern for content links
    linkPattern: /\[([^\]]+)\]\(([^)]+)\)/g,
    
    // Pattern for image references
    imagePattern: /!\[([^\]]*)\]\(([^)]+)\)/g
};

async function validateMarkdownFile(filePath) {
    const content = await fs.readFile(filePath, 'utf-8');
    const results = {
        filePath: filePath,
        errors: [],
        warnings: []
    };
    
    // Check minimum content length
    if (content.length < validationRules.minContentLength) {
        results.errors.push(`Content too short: ${content.length} characters (minimum: ${validationRules.minContentLength})`);
    }
    
    // Check for proper markdown structure
    if (!content.includes('# ')) {
        results.warnings.push('No main heading found (should have at least one H1)');
    }
    
    // Check for broken links or images
    const links = content.match(validationRules.linkPattern) || [];
    const images = content.match(validationRules.imagePattern) || [];
    
    for (const link of links) {
        const [fullMatch, text, url] = link;
        if (url.startsWith('./') || url.startsWith('../')) {
            // Relative link - check if the file exists
            const linkPath = path.resolve(path.dirname(filePath), url);
            try {
                await fs.access(linkPath);
            } catch (err) {
                results.errors.push(`Broken link: ${url} (resolved to ${linkPath})`);
            }
        }
    }
    
    for (const image of images) {
        const [fullMatch, altText, url] = image;
        if (url.startsWith('./') || url.startsWith('../')) {
            // Relative image - check if the file exists
            const imagePath = path.resolve(path.dirname(filePath), url);
            try {
                await fs.access(imagePath);
            } catch (err) {
                results.errors.push(`Missing image: ${url} (resolved to ${imagePath})`);
            }
        }
    }
    
    return results;
}

async function validateAllContent() {
    console.log('🔍 Starting content validation...');
    
    try {
        const errors = [];
        const warnings = [];
        let validFiles = 0;
        let totalFiles = 0;
        
        // Read all markdown files
        const files = await readMarkdownFiles(DOCS_DIR);
        console.log(`📖 Found ${files.length} markdown files to validate`);
        
        for (const file of files) {
            console.log(`📝 Validating: ${file}`);
            totalFiles++;
            
            const result = await validateMarkdownFile(file);
            
            if (result.errors.length > 0 || result.warnings.length > 0) {
                for (const error of result.errors) {
                    errors.push(`${result.filePath}: ${error}`);
                }
                for (const warning of result.warnings) {
                    warnings.push(`${result.filePath}: ${warning}`);
                }
            } else {
                validFiles++;
            }
        }
        
        console.log('\n📊 Validation Results:');
        console.log(`✅ Valid files: ${validFiles}`);
        console.log(`❌ Files with errors: ${errors.length}`);
        console.log(`⚠️  Files with warnings: ${warnings.length}`);
        
        if (errors.length > 0) {
            console.log('\n❌ ERRORS:');
            for (const error of errors) {
                console.log(`  - ${error}`);
            }
        }
        
        if (warnings.length > 0) {
            console.log('\n⚠️ WARNINGS:');
            for (const warning of warnings) {
                console.log(`  - ${warning}`);
            }
        }
        
        if (errors.length === 0) {
            console.log('\n🎉 All content passed validation!');
            return true;
        } else {
            console.log('\n❌ Some content failed validation.');
            return false;
        }
    } catch (error) {
        console.error('❌ Error during content validation:', error);
        process.exit(1);
    }
}

async function readMarkdownFiles(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    let files = [];
    
    for (let entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
            files = files.concat(await readMarkdownFiles(fullPath));
        } else if (entry.isFile() && path.extname(entry.name) === '.md') {
            files.push(fullPath);
        }
    }
    
    return files;
}

// Run validation
validateAllContent().then(success => {
    if (!success) {
        process.exit(1);
    }
});