import java.io.IOException;

// import java.util.Comparator;
// import java.util.Collection;
// import java.util.Map;
// import java.util.TreeMap;
// import java.util.List;
import java.util.*;

// import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.*;

// import org.dblp.mmdb.Mmdb;
// import org.dblp.mmdb.Field;
// import org.dblp.mmdb.FieldReader;
// import org.dblp.mmdb.Person;
// import org.dblp.mmdb.PersonName;
// import org.dblp.mmdb.Publication;
// import org.dblp.mmdb.RecordDb;
// import org.dblp.mmdb.RecordDbInterface;
// import org.dblp.mmdb.TableOfContents;
import org.dblp.mmdb.*;
import org.xml.sax.SAXException;

class Selfciters {

  public static List<String> getCitersOfPublications(Mmdb database, String key) { // done + tested
    // returns a list of keys of all publication who have cited the provided key
    System.out.println("Seeing all the papers where " + key + " was cited");
    List<String> publicationsWhichSiteThisPaper = database.publications()
      .filter(r -> r.getFieldReader().contains("cite", key))
      .map(r -> r.getKey())
      .collect(toList());
    return publicationsWhichSiteThisPaper;
  }

  public static List<String> getAuthorsOfPublication(Mmdb database, String key) { // done + tested
    // returns a list of keys all authors of a particular publication
    System.out.println("getting authors of: " + key);
    List<String> authors = database.getPublication(key)
      .names()
      .map(n -> n.getPerson().getKey())
      .collect(toList());
    return authors;
  }

  public static List<String> getPublicationsByAuthor(Mmdb database, String key) { // done + tested
    // returns a list of keys of publications from the key of a person/author
    System.out.println("getting publications of: " + key);
    List<String> publications = database.getPerson(key)
      .publications()
      .map(p -> p.getKey())
      .collect(toList());
    return publications;
  }

  public static double getSelfCitationPercentageOfAuthor(Mmdb database, String key){ // done + tested
    List<String> publications = getPublicationsByAuthor(database, key);

    // number of publications
    System.out.println("Number of publications: " + publications.size());

    int totalCitations = 0;
    int selfCitations = 0;

    // generating an iterator and using it to loop through publications
    ListIterator<String> publicationsIterator = publications.listIterator();
    while(publicationsIterator.hasNext()) {
      // getting all the citer publication keys
      List<String> citerKeys = getCitersOfPublications(
          database,
          publicationsIterator.next()
          );
      totalCitations += citerKeys.size();

      // looping though these citations and getting their authors
      ListIterator<String> citerKeysIterator = citerKeys.listIterator();
      while(citerKeysIterator.hasNext()) {
        List<String> authors = getAuthorsOfPublication(
            database,
            citerKeysIterator.next()
            );
        // checking if out original author is here
        if(authors.contains(key)) {
          selfCitations += 1;
        }
      }
    }
    System.out.println("Total Citations: " + totalCitations);
    System.out.println("Self Citations: " + selfCitations);
    return ((double)selfCitations *100 / (double)totalCitations);
  }

  public static void main(String[] args) throws IOException, SAXException {

    // to handle the large size of the dataset, setting  entity expansion to 10**7
    System.setProperty("entityExpansionLimit", "10000000");

    // in case the paths aren't provided
    if (args.length < 1) {
      System.out.format("Usage: java %s <dblp-xml>\n", Selfciters.class.getName());
      System.exit(0);
    }

    // Storing the filename arguments
    String dblpXmlFilename = args[0];
    String dblpDtdFilename = args[1];

    // Loading the database
    Mmdb database = new Mmdb(dblpXmlFilename, dblpDtdFilename,true); // < 2min or 120s

    // testing our precious functions

    System.out.println(getCitersOfPublications(database,  "journals/cacm/Codd70")); // 14+ seconds
    System.out.println(getPublicationsByAuthor(database, "homepages/c/EFCodd"));// almost no time
    System.out.println(getAuthorsOfPublication(database, "journals/cacm/Codd70")); // almost no time

    System.out.println("SelfCitation percent: " + getSelfCitationPercentageOfAuthor(database, "homepages/c/EFCodd") + " %");
    // Total Citations: 1465
    // Self Citations: 3
    // SelfCitation percent: 0.20477815699658702 %
    // That took a total of: 288191ms = 288s = 4min 48s
  }
}
