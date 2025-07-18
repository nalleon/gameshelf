package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Details;
import es.gameshelf.model.entities.abstracts.DetailsEntity;
import jakarta.persistence.Entity;
import jakarta.persistence.NamedQuery;
import jakarta.persistence.Table;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name="editions")
@NamedQuery(name="EditionEntity.findAll", query="SELECT r FROM EditionEntity r")
public class EditionEntity extends DetailsEntity {
    /**
     * Default constructor of the class
     */
    public EditionEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the edition
     */
    public EditionEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the edition
     */
    public EditionEntity(String name) {
        super(name);
    }

    /**
     * Constructor of the class
     * @param name of the edition
     * @param additionalText of the edition
     */
    public EditionEntity(String name, String additionalText) {
        super(name, additionalText);
    }

    /**
     * Constructor of the class
     * @param id of the edition
     * @param name of the edition
     * @param additionalText of the edition
     */
    public EditionEntity(int id, String name, String additionalText) {
        super(id, name, additionalText);
    }
}
