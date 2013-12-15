/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pagerankinvertedindex;

import ir.vsr.DocumentIterator;
import ir.vsr.InvertedIndex;
import java.io.File;

/**
 *
 * @author Paweł
 */
public class PageRankInvertedIndex extends InvertedIndex {

    private double weight = 0.0;
    
    public PageRankInvertedIndex(File dirFile, short docType, boolean stem, boolean feedback, double weight) {
        super(dirFile, docType, stem, feedback);
        this.weight = weight;
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String dirName = args[args.length - 1];
        short docType = DocumentIterator.TYPE_TEXT;
        boolean stem = false, feedback = false;
        double weight = 0.0;
        for (int i = 0; i < args.length - 1; i++) {
            String flag = args[i];
            if (flag.equals("-weight")) // Create HTMLFileDocuments to filter HTML tags
            {
                weight = Double.parseDouble(args[i+1]);
            } 
        }
        // Create an inverted index for the files in the given directory.
        PageRankInvertedIndex index = new PageRankInvertedIndex(new File(dirName), docType, stem, feedback, weight);
        // index.print();
        // Interactively process queries to this index.
        index.processQueries();
    }
}
