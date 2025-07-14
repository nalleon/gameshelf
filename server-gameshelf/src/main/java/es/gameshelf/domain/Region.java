package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class Region extends Details {
    /**
     * Default constructor of the class
     */
    public Region() {
    }

    /**
     * Constructor of the class
     * @param id of the region
     */
    public Region(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the region
     */
    public Region(String name) {
        super(name);
    }

    /**
     * Constructor of the class
     * @param name of the region
     * @param additionalText of the region
     */
    public Region(String name, String additionalText) {
        super(name, additionalText);
    }

    /**
     * Constructor of the class
     * @param id of the region
     * @param name of the region
     * @param additionalText of the region
     */
    public Region(int id, String name, String additionalText) {
        super(id, name, additionalText);
    }
}
