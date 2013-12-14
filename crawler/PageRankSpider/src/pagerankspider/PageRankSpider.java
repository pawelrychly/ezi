/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pagerankspider;


import ir.utilities.MoreMath;
import ir.utilities.MoreString;
import ir.webutils.Graph;
import ir.webutils.HTMLPage;
import ir.webutils.Link;
import ir.webutils.LinkExtractor;
import ir.webutils.Node;
import ir.webutils.PathDisallowedException;
import ir.webutils.Spider;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 *
 * @author Paweł
 */
public class PageRankSpider extends Spider {
    
    private Graph graph = new Graph();
    
    //private HashMap<String, String> map = new HashMap<String, String>();

    public File getSaveDir() {
        return saveDir;
    }
    
    
    
    private Boolean checkLink(Link link) {
        
        if (!linkToHTMLPage(link)) {
            return false;
        }
	    HTMLPage currentPage = null;
	    // Use the page retriever to get the page
	    try {
		currentPage = webpr.getHTMLPage(link);
	    }
	    catch (PathDisallowedException e) {
            return false;
        }
	    if (currentPage.empty()) {
            return false;
	    }
	    if (!currentPage.indexAllowed()) {
            return false;
        }
        return true;
    }
    
    @Override
    protected void processPage(HTMLPage page) {
	// Extract links in order to change them to absolute URL's
        new LinkExtractor(page).extractLinks();
        String path = page.getLink().getURL().getPath();
        int index = path.lastIndexOf("/");
        String fileName = path.substring(index + 1);
        
        List links = page.getOutLinks();
        Iterator i = links.iterator();
        while (i.hasNext()) {
            Link link = (Link) i.next();
            if (checkLink(link)) {
                String toPath = link.getURL().getPath();
                index = toPath.lastIndexOf("/");
                String fileName2 = toPath.substring(index + 1);
                this.graph.addEdge(fileName, fileName2);
            }
        }
        //graph.addEdge(fileName, fileName);
        
       //String name = "P" + MoreString.padWithZeros(count,(int)Math.floor(MoreMath.log(maxCount, 10)) + 1);

        page.writeAbsolute(saveDir, fileName);
        
    }

   
    
    public Graph getGraph() {
        return graph;
    }
    
    public static void main(String args[]) {
        PageRankSpider pageRankSpider = new PageRankSpider();
        pageRankSpider.go(args);
        
        
        Graph graph = pageRankSpider.getGraph();
        
        int length = graph.nodeArray().length;
        System.out.println("--------END------------");
        
        for (int i = 0; i < length; i++) {
            Node node = graph.nodeArray()[i];
            ArrayList<Node> outNodes = node.getEdgesOut();
            System.out.print(node.toString() + " -> [");
            
            for (Node outNode: outNodes) {
                System.out.print(outNode.toString()+ ",");
            }
            System.out.println("]");
            
        }
        PageRankFile.countPageRanks(graph, pageRankSpider.getSaveDir().toString());
        
    }
  
    
}
