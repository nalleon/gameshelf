package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Format;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IFormatService {
    Format add(String name);
    List<Format> findAll();
    Format findById(Integer id);
    Format findByName(String name);
    boolean delete(Integer id);
    Format update(Integer id, String name);
}
