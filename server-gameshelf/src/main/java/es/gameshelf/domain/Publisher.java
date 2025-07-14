package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class Publisher extends Classification {
    /**
     * Default constructor of the class
     */
    public Publisher() {
    }

    /**
     * Constructor of the class
     * @param id of the publisher
     */
    public Publisher(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the publisher
     */
    public Publisher(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the publisher
     * @param name of the publisher
     */
    public Publisher(int id, String name) {
        super(id, name);
    }
}
