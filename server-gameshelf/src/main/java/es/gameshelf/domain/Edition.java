package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class Edition extends Details {
    /**
     * Default constructor of the class
     */
    public Edition() {
    }

    /**
     * Constructor of the class
     * @param id of the edition
     */
    public Edition(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the edition
     */
    public Edition(String name) {
        super(name);
    }

    /**
     * Constructor of the class
     * @param name of the edition
     * @param additionalText of the edition
     */
    public Edition(String name, String additionalText) {
        super(name, additionalText);
    }

    /**
     * Constructor of the class
     * @param id of the edition
     * @param name of the edition
     * @param additionalText of the edition
     */
    public Edition(int id, String name, String additionalText) {
        super(id, name, additionalText);
    }
}
