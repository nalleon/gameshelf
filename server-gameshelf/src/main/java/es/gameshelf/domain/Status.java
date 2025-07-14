package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class Status extends Details {
    /**
     * Default constructor of the class
     */
    public Status() {
    }

    /**
     * Constructor of the class
     * @param id of the status
     */
    public Status(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the status
     */
    public Status(String name) {
        super(name);
    }

    /**
     * Constructor of the class
     * @param name of the status
     * @param additionalText of the status
     */
    public Status(String name, String additionalText) {
        super(name, additionalText);
    }

    /**
     * Constructor of the class
     * @param id of the status
     * @param name of the status
     * @param additionalText of the status
     */
    public Status(int id, String name, String additionalText) {
        super(id, name, additionalText);
    }
}
