import java.io.IOException;

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

class GetCitersDataOfPublication implements Runnable {
  private volatile int citations = 0;
  private volatile int selfCitations = 0;
  private volatile Mmdb database;
  private volatile String publicationKey;
  private volatile String authorKey;

  //  constructor
  public GetCitersDataOfPublication(Mmdb inputDatabase, String inputPublicationKey, String inputAuthorKey) {
    database = inputDatabase;
    publicationKey = inputPublicationKey;
    authorKey = inputAuthorKey;
  }

  public void run() {
    // finding all publications which cite
    List<String> citerPublicationKeys = database.publications()
      .filter(r-> r.getFieldReader().contains("cite", publicationKey))
      .map(r -> r.getKey())
      .collect(toList());

    citations = citerPublicationKeys.size();
    // looping through all the cited publications
    for(String citation:citerPublicationKeys) {
      //getting authors
      List<String> authors = database.getPublication(citation)
        .names()
        .map(n -> n.getPerson().getKey())
        .collect(toList());
      if (authors.contains(authorKey)) {
        selfCitations += 1;
      }
    }
  }
  public int getCitationCount() {
    return citations;
  }
  public int getSelfCitationCount() {
    return selfCitations;
  }
}

public class Selfciters {

  public static List<String> getCitersOfPublications(Mmdb database, String key) { // done + tested
    // returns a list of keys of all publication who have cited the provided key
    List<String> publicationsWhichCiteThisPaper = database.publications()
      .filter(r -> r.getFieldReader().contains("cite", key))
      .map(r -> r.getKey())
      .collect(toList());
    return publicationsWhichCiteThisPaper;
  }

  public static List<String> getAuthorsOfPublication(Mmdb database, String key) { // done + tested
    // returns a list of keys all authors of a particular publication
    List<String> authors = database.getPublication(key)
      .names()
      .map(n -> n.getPerson().getKey())
      .collect(toList());
    return authors;
  }

  public static List<String> getPublicationsByAuthor(Mmdb database, String key) { // done + tested
    // returns a list of keys of publications from the key of a person/author
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

  public static double  getSelfCitationPercentageOfAuthorByThreading(Mmdb database, String key) { // done
    List<String> publications = getPublicationsByAuthor(database, key);

    // number of publications
    System.out.println("Number of publications: " + publications.size());

    int totalCitations = 0;
    int selfCitations = 0;

    List<GetCitersDataOfPublication> objects = new ArrayList<GetCitersDataOfPublication>();
    List<Thread> threads = new ArrayList<Thread>();

    // adding threads
    for(String publication:publications) {
      // generating object
      GetCitersDataOfPublication object = new GetCitersDataOfPublication(database, publication,key);
      objects.add(object);
      // putting it in a thread
      threads.add(new Thread(object));
    }

    // starting all threads
    System.out.println("Starting all threads...");
    for(Thread thread:threads) {
      thread.start();
    }

    // waiting for all the threads to complete
    System.out.println("All threads have been started, waiting for completion.");
    for(Thread thread:threads) {
      try{
        thread.join();
      } catch(InterruptedException e){
        System.out.println("there was a messup");
      }
    }

    // collecting all the data
    System.out.println("All threads have been completed, collecting data...");
    for(GetCitersDataOfPublication object:objects) {
      totalCitations += object.getCitationCount();
      selfCitations += object.getSelfCitationCount();
    }

    System.out.println("Data has been collected \n\n Result:");
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
    System.out.println("Loading XML into Memory...");
    long startTime = System.currentTimeMillis();
    Mmdb database = new Mmdb(dblpXmlFilename, dblpDtdFilename,false); // < 2min or 120s
    long endTime = System.currentTimeMillis();
    long duration = (endTime - startTime);
    System.out.println("That took a total of: " + duration + " ms");

    // testing our precious functions
    // System.out.println(getCitersOfPublications(database,  "journals/cacm/Codd70")); // 14+ seconds
    // System.out.println(getPublicationsByAuthor(database, "homepages/c/EFCodd"));// almost no time
    // System.out.println(getAuthorsOfPublication(database, "journals/cacm/Codd70")); // almost no time

    // System.out.println("Starting single threaded version");
    // startTime = System.currentTimeMillis();
    System.out.println("SelfCitation percent on a single thread: " + getSelfCitationPercentageOfAuthor(database, "homepages/c/EFCodd") + " %");
    // endTime = System.currentTimeMillis();
    // duration = (endTime - startTime);
    // System.out.println("That took a total of: " + duration + " ms");

    // Total Citations: 1465
    // Self Citations: 3
    // SelfCitation percent: 0.20477815699658702 %
    // That took a total of: 288191ms = 288s = 4min 48s

    System.out.println("Starting multi threaded threaded version");
    startTime = System.currentTimeMillis();
    System.out.println("SelfCitation percent by threading: " + getSelfCitationPercentageOfAuthorByThreading(database, "homepages/c/EFCodd") + " %");
    endTime = System.currentTimeMillis();
    duration = (endTime - startTime);
    System.out.println("That took a total of: " + duration + " ms");
  }
}
