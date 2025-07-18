package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Details;
/**
 * @author Nabil L. A. @nalleon
 */
public class StatusEntity extends Details {
    /**
     * Default constructor of the class
     */
    public StatusEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the status
     */
    public StatusEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the status
     */
    public StatusEntity(String name) {
        super(name);
    }

    /**
     * Constructor of the class
     * @param name of the status
     * @param additionalText of the status
     */
    public StatusEntity(String name, String additionalText) {
        super(name, additionalText);
    }

    /**
     * Constructor of the class
     * @param id of the status
     * @param name of the status
     * @param additionalText of the status
     */
    public StatusEntity(int id, String name, String additionalText) {
        super(id, name, additionalText);
    }
}
